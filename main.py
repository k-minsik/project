import cv2
import mediapipe as mp
import flask
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

reps = 0 
status = "Start"

def get_angle(top, mid, bottom):
    angle = math.degrees(math.atan2(bottom[1] - mid[1], bottom[0] - mid[0]) - math.atan2(top[1] - mid[1], top[0] - mid[0]))

    if angle > 180.0:
        angle = 360 - angle

    return angle

cap = cv2.VideoCapture('squat.mp4')
# cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        results = pose.process(frame)
    
        landmarks = results.pose_landmarks.landmark
        
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)               
        
        rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        
        angle = get_angle(rightHip, rightKnee, rightAnkle)
        print(angle)
        
        if angle < 70:
            status = "SQUAT"
        if angle > 160 and status == 'SQUAT':
            status = "UP"
            reps +=1
            
        cv2.rectangle(frame, (0,0), (225,73), (245,117,16), -1)
        
        cv2.putText(frame, 'REPS', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(reps), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        cv2.putText(frame, 'STATUS', (65,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame, status, (60,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        cv2.imshow('Training Censor', frame)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()