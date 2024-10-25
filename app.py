from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
import mediapipe as mp
from absl import logging
import json
import threading
import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Add chatbot configuration
ONDEMAND_API_KEY = os.getenv('ONDEMAND_API_KEY')
EXTERNAL_USER_ID = os.getenv('EXTERNAL_USER_ID')
CHAT_API_BASE_URL = 'https://api.on-demand.io/chat/v1'


# Initialize MediaPipe
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Global variables for tracking
counter = 0
position = ""
exercise_active = False
current_exercise = None
camera_lock = threading.Lock()

class VideoCamera:
    def __init__(self):
        self.video = None
        self.is_running = False
    
    def start(self):
        if self.video is None:
            self.video = cv2.VideoCapture(0)
            self.is_running = True
    
    def stop(self):
        if self.video is not None:
            self.video.release()
            self.video = None
            self.is_running = False
    
    def get_frame(self):
        if self.video is None:
            self.start()
        
        success, img = self.video.read()
        if not success:
            return None
        
        return img

camera = VideoCamera()

def generate_frames(exercise_func):
    global counter, position, exercise_active
    
    while True:
        with camera_lock:
            frame = camera.get_frame()
            if frame is None:
                continue
            
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)
            
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                points = {}
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    points[id] = (cx, cy)
                
                # Call the specific exercise tracking function
                if exercise_func == "pushup":
                    track_pushup(points)
                elif exercise_func == "pullup":
                    track_pullup(points)
                elif exercise_func == "bicep_curls":
                    track_curls(points)
                elif exercise_func == "shoulder_raises":
                    track_shoulder_raises(points)
                elif exercise_func == "press":
                    track_press(points)
                elif exercise_func == "squats":
                    track_squats(points)
                elif exercise_func == "deadlift":
                    track_deadlift(points)
                elif exercise_func == "lunges":
                    track_lunges(points)
                
                # Draw counter and position
                cv2.putText(frame, f"{counter} {position}", (100, 150), 
                           cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        time.sleep(0.033)  # Limit frame rate to ~30 fps

def track_pushup(points):
    global counter, position, exercise_active
    
    if not exercise_active and points[12][1] < points[14][1]:
        position = "UP"
        exercise_active = True
        counter += 1
    elif exercise_active and points[12][1] - 60 > points[14][1]:
        position = "DOWN"
        exercise_active = False

def track_pullup(points):
    global counter, position, exercise_active
    
    if not exercise_active and (points[12][1] - 50 < points[16][1] and points[11][1] - 50 < points[15][1]):
        position = "UP"
        exercise_active = True
        counter += 1
    elif exercise_active and (points[12][1] - 200 > points[16][1] and points[11][1] - 200 > points[15][1]):
        position = "DOWN"
        exercise_active = False

def track_curls(points):
    global counter, position, exercise_active
    
    if not exercise_active and (points[14][1] - 50 > points[16][1] and points[13][1] - 50 > points[15][1]):
        position = "UP"
        exercise_active = True
        counter += 1
    elif exercise_active and (points[14][1] + 70 < points[16][1] and points[15][1] + 70 > points[13][1]):
        position = "DOWN"
        exercise_active = False

def track_shoulder_raises(points):
    global counter, position, exercise_active
    
    if not exercise_active and (points[14][1] + 30 < points[12][1] and points[13][1] + 30 < points[11][1]):
        position = "UP"
        exercise_active = True
        counter += 1
    elif exercise_active and (points[14][1] - 30 > points[12][1] and points[13][1] - 30 > points[11][1]):
        position = "DOWN"
        exercise_active = False

def track_press(points):
    global counter, position, exercise_active
    
    if not exercise_active and (points[12][1] - 50 < points[16][1] and points[11][1] - 50 < points[15][1]):
        position = "DOWN"
        exercise_active = True
        counter += 1
    elif exercise_active and (points[12][1] - 200 > points[16][1] and points[11][1] - 200 > points[15][1]):
        position = "UP"
        exercise_active = False

def track_squats(points):
    global counter, position, exercise_active
    
    if not exercise_active and points[24][1] > points[26][1]:
        position = "DOWN"
        exercise_active = True
    elif exercise_active and points[24][1] + 50 < points[26][1]:
        position = "UP"
        exercise_active = False
        counter += 1

def track_deadlift(points):
    global counter, position, exercise_active
    
    if not exercise_active and points[25][1] > points[15][1]:
        position = "UP"
        exercise_active = True
    elif exercise_active and points[25][1] + 70 < points[15][1]:
        position = "DOWN"
        exercise_active = False
        counter += 1

def track_lunges(points):
    global counter, position, exercise_active
    
    if not exercise_active and points[27][1] > points[26][1]:
        position = "Right Down"
        exercise_active = True
        counter += 1
    elif exercise_active and points[28][1] > points[25][1]:
        position = "Left Down"
        exercise_active = False
        counter += 1

def create_chat_session():
    create_session_url = f'{CHAT_API_BASE_URL}/sessions'
    headers = {
        'apikey': ONDEMAND_API_KEY
    }
    body = {
        "pluginIds": [],
        "externalUserId": EXTERNAL_USER_ID
    }
    
    try:
        response = requests.post(create_session_url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()['data']['id']
    except requests.exceptions.RequestException as e:
        print(f"Error creating chat session: {e}")
        return None

def submit_chat_query(session_id, query):
    submit_query_url = f'{CHAT_API_BASE_URL}/sessions/{session_id}/query'
    headers = {
        'apikey': ONDEMAND_API_KEY
    }
    body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": query,
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }
    
    try:
        response = requests.post(submit_query_url, headers=headers, json=body)
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the answer from the nested response
        if 'data' in response_data and 'answer' in response_data['data']:
            return {'message': response_data['data']['answer']}
        else:
            return {'error': 'Invalid response format'}
            
    except requests.exceptions.RequestException as e:
        print(f"Error submitting query: {e}")
        return {'error': str(e)}

@app.route('/api/chat/query', methods=['POST'])
def chat_query():
    data = request.json
    session_id = data.get('session_id')
    query = data.get('query')
    
    if not session_id or not query:
        return jsonify({'error': 'Missing session_id or query'}), 400
    
    response = submit_chat_query(session_id, query)
    if response:
        return jsonify(response)
    return jsonify({'error': 'Failed to get response'}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/exercise/<exercise_type>')
def exercise(exercise_type):
    global current_exercise, counter, position
    current_exercise = exercise_type
    counter = 0  # Reset counter when starting new exercise
    position = ""
    return render_template('exercise.html', exercise=exercise_type)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(current_exercise),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_count')
def get_count():
    global counter, position
    return jsonify({'count': counter, 'position': position})

# New routes for chatbot
@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/chat/session', methods=['POST'])
def create_session():
    session_id = create_chat_session()
    if session_id:
        return jsonify({'session_id': session_id})
    return jsonify({'error': 'Failed to create chat session'}), 500

# @app.route('/api/chat/query', methods=['POST'])
# def chat_query():
#     data = request.json
#     session_id = data.get('session_id')
#     query = data.get('query')
    
#     if not session_id or not query:
#         return jsonify({'error': 'Missing session_id or query'}), 400
    
#     response = submit_chat_query(session_id, query)
#     if response:
#         return jsonify(response)
#     return jsonify({'error': 'Failed to get response'}), 500

@app.route('/start_camera')
def start_camera():
    camera.start()
    return jsonify({'status': 'success'})

@app.route('/stop_camera')
def stop_camera():
    camera.stop()
    return jsonify({'status': 'success'})



@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', error_code=403, 
                         error_message="Access to camera was denied. Please allow camera access and refresh the page."), 403

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500,
                         error_message="An internal error occurred. Please try refreshing the page."), 500

if __name__ == '__main__':
    app.run(debug=True, port=5100)