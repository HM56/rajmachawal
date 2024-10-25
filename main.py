import cv2
import mediapipe as mp

#import tensorflow as tf

from absl import logging
logging.use_absl_handler()

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def PushUp():
    cap = cv2.VideoCapture(0)
    pos = ""
    UP = False
    counter = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,lm,cx,cy)
                points[id] = (cx, cy)

            cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[14], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[11], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[13], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)

            if not UP and points[12][1] < points[14][1]:
                pos = "UP"
                print(pos)
                UP = True
                counter += 1
                print(counter, "\n------------------\n")
            elif UP and points[12][1] - 60 > points[14][1]:
                pos = "DOWN"
                print(pos)
                UP = False
            elif points[15][0] < points[16][0]:
                print("Exit\nThanks for using this program")
                return
            elif points[11][0] < points[16][0]:
                goto()
        cv2.putText(img, str(counter) + "  " + pos, (100, 150), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
        cv2.imshow('img', img)
        cv2.waitKey(1)
def PullUp():
    cap = cv2.VideoCapture(0)
    pos = ""
    UP = False
    counter = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,lm,cx,cy)
                points[id] = (cx, cy)

            cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[11], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)

            if not UP and (points[12][1] - 50 < points[16][1] and points[11][1] - 50 < points[15][1]):
                pos = "UP"
                print(pos)
                UP = True
                counter += 1
                print(counter, "\n------------------\n")
            elif UP and (points[12][1] - 200 > points[16][1] and points[11][1] - 200 > points[15][1]):
                pos = "DOWN"
                print(pos)
                UP = False
            elif points[15][0] < points[16][0]:
                print("Exit\nThanks for using this program")
                cap.release()
                cv2.destroyAllWindows()
                return
            elif points[11][0] < points[16][0]:
                goto()
        cv2.putText(img, str(counter) + "  " + pos, (100, 150), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
        cv2.imshow('img', img)
        cv2.waitKey(1)
def Curls():
    cap = cv2.VideoCapture(0)
    pos = ""
    UP = False
    counter = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,lm,cx,cy)
                points[id] = (cx, cy)

            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[14], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[13], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)

            if not UP and points[14][1] - 50 > points[16][1]:
                pos = "UP"
                print(pos)
                UP = True
                counter += 1
                print(counter, "\n------------------\n")
            elif UP and points[14][1] + 70 < points[16][1]:
                pos = "DOWN"
                print(pos)
                UP = False
            elif points[15][0] < points[16][0]:
                print("Exit\nThanks for using this program")
                return
            elif points[11][0] < points[16][0]:
                goto()
        cv2.putText(img, str(counter) + "  " + pos, (100, 150), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
        cv2.imshow('img', img)
        cv2.waitKey(1)
def Shoulder_raises():
    cap = cv2.VideoCapture(0)
    pos = ""
    UP = False
    counter = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,lm,cx,cy)
                points[id] = (cx, cy)

            cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[14], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[11], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[13], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)

            if not UP and points[14][1] + 30 < points[12][1]:
                pos = "UP"
                print(pos)
                UP = True
                counter += 1
                print(counter, "\n------------------\n")
            elif UP and points[14][1] - 30 > points[12][1]:
                pos = "DOWN"
                print(pos)
                UP = False
            elif points[15][0] < points[16][0]:
                print("Exit\nThanks for using this program")
                return
            elif points[11][0] < points[16][0]:
                goto()
        cv2.putText(img, str(counter) + "  " + pos, (100, 150), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
        cv2.imshow('img', img)
        cv2.waitKey(1)
def Squats():
    cap = cv2.VideoCapture(0)
    pos = ""
    UP = False
    counter = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,lm,cx,cy)
                points[id] = (cx, cy)

            cv2.circle(img, points[24], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[26], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[23], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[25], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)

            if not UP and points[24][1] > points[26][1]:
                pos = "DOWN"
                print(pos)
                UP = True
            elif UP and points[24][1] + 50 < points[26][1]:
                pos = "UP"
                print(pos)
                UP = False
                counter += 1
                print(counter, "\n------------------\n")
            elif points[15][0] < points[16][0]:
                print("Exit\nThanks for using this program")
                return
            elif points[11][0] < points[16][0]:
                goto()
        cv2.putText(img, str(counter) + "  " + pos, (100, 150), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
        cv2.imshow('img', img)
        cv2.waitKey(1)
def Press():
    cap = cv2.VideoCapture(0)
    pos = ""
    UP = False
    counter = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,lm,cx,cy)
                points[id] = (cx, cy)

            cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[11], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)

            if not UP and (points[12][1] - 50 < points[16][1] and points[11][1] - 50 < points[15][1]):
                pos = "DOWN"
                print(pos)
                UP = True
                counter += 1
                print(counter, "\n------------------\n")
            elif UP and (points[12][1] - 200 > points[16][1] and points[11][1] - 200 > points[15][1]):
                pos = "UP"
                print(pos)
                UP = False
            elif points[15][0] < points[16][0]:
                print("Exit\nThanks for using this program")
                return
            elif points[11][0] < points[16][0]:
                goto()
        cv2.putText(img, str(counter) + "  " + pos, (100, 150), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
        cv2.imshow('img', img)
        cv2.waitKey(1)
def deadlift():# check karna
    cap = cv2.VideoCapture(0)
    pos = ""
    UP = False
    counter = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,lm,cx,cy)
                points[id] = (cx, cy)

            cv2.circle(img, points[23], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[25], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[24], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[26], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)

            if not UP and points[25][1] > points[15][1]:
                pos = "UP"
                print(pos)
                UP = True
            elif UP and points[25][1] + 70  < points[15][1]:
                pos = "DOWN"
                print(pos)
                UP = False
                counter += 1
                print(counter, "\n------------------\n")
            elif points[15][0] < points[16][0]:
                print("Exit\nThanks for using this program")
                return
            elif points[11][0] < points[16][0]:
                goto()
        cv2.putText(img, str(counter) + "  " + pos, (100, 150), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
        cv2.imshow('img', img)
        cv2.waitKey(1)
def lunges():
    cap = cv2.VideoCapture(0)
    pos = ""
    UP = False
    counter = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,lm,cx,cy)
                points[id] = (cx, cy)

            cv2.circle(img, points[24], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[26], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[23], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[25], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[27], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[28], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[15], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)

            if not UP and points[27][1] > points[26][1]:
                pos = "Right Down"
                print(pos)
                UP = True
                counter +=1
            elif UP and points[28][1] > points[25][1]:
                pos = "Left Down"
                print(pos)
                UP = False
                counter += 1
                print(counter, "\n------------------\n")
            elif points[15][0] < points[16][0]:
                print("Exit\nThanks for using this program")

                return
            elif points[11][0] < points[16][0]:
                goto()
        cv2.putText(img, str(counter) + "  " + pos, (100, 150), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255))
        cv2.imshow('img', img)
        cv2.waitKey(1)
def goto():
    exercise_input = int(input("Instructions -:\n-Place you camera directly in front of you."
                               "\n-If you want to change your Exercise , tap on you left shoulder "
                               "with your right hand.\n"
                               "with your left hand.\n-If you want to quit ,"
                               " make a cross with your arms.\n-Reps are only count by right hand in some "
                               "exercise.\n\n\n"
                               "Choose your your type of Exerice-\n"
                               "1) Weighted exercise \n2) Non Weighted exercise"
                               "\nEnter a valid number from above"))
    if exercise_input== 2 :
        nwex= int(input("Enter your Weighted exercise:\n1)Push Up \n2)Pull up \n3)Squats"
                     "\n4)Lunges"
                     "\nEnter a valid number from above"))
        if nwex == 1:#Push UP
            PushUp()
        elif nwex == 2:#pull up
            PullUp()
        elif nwex == 3:#squats
            Squats()
        elif nwex  == 4:#lunges
            Lunges()
        else:
            print("wrong input")
            ans = int(input("If you want to quit press 1\nIf you want to continue press 0"))
            if ans == 1:
                print("Thanks for using this program")
                cap.release()
                cv2.destroyAllWindows()
                return
            elif ans == 0:
                goto()
    if exercise_input==1:
        wex= int(input("Enter your Non Weighted exercise:\n1)Bicep Curls"
                     "\n2)Shoulder raises(any type)"
                     "\n3)Shoulder/inclined Press \n4)Deadlift"
                     "\nEnter a valid number from above"))
        if wex == 1:  # curls
            Curls()
        elif wex == 2:  # shoulder raises
            Shoulder_raises()
        elif wex == 3:  # press
            Press()
        elif wex == 4: #deadlift
            deadlift()
        else:
            print("wrong input")
            ans = int(input("If you want to quit press 1\nIf you want to continue press 0"))
            if ans == 1:
                print("Thanks for using this program")
                cap.release()
                cv2.destroyAllWindows()
                return
            elif ans == 0:
                goto()
    else:
        print("wrong input")
        ans = int(input("If you want to quit press 1\nIf you want to continue press 0"))
        if ans == 1:
            print("Thanks for using this program")
            cap.release()
            cv2.destroyAllWindows()
            return
        elif ans == 0:
            goto()
goto()
tf.get_logger().setLevel('ERROR')  # Set logging level to ERROR to avoid warnings
