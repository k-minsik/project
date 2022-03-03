import cv2
import mediapipe as mp
import count

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

reps = 0 
status = "Start"


cap = cv2.VideoCapture('squat.mp4')
# cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        results = pose.process(frame)
    
        landmarks = results.pose_landmarks.landmark
        
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)               
        
        rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        
        kneeAngle = (count.get_angle(rightHip, rightKnee, rightAnkle) + count.get_angle(leftHip, leftKnee, leftAnkle)) / 2
        hipAngle = (count.get_angle(rightShoulder, rightHip, rightKnee) + count.get_angle(leftShoulder, leftHip, leftKnee)) / 2
        elbowAngle = (count.get_angle(rightShoulder, rightElbow, rightWrist) + count.get_angle(leftShoulder, leftElbow, leftWrist)) / 2

        
        #Squat
        hipAngle, kneeAngle, reps, status = count.squat(hipAngle, kneeAngle, reps, status)

        #BenchPress
        # elbowAngle, reps, status = count.benchpress(elbowAngle, reps, status)

        #DeadLift
        # hipAngle, kneeAngle, reps, status = count.deadlift(hipAngle, kneeAngle, reps, status)

        cv2.rectangle(frame, (400,760), (534,960), (255,255,255), -1)
        
        cv2.putText(frame, 'REPS', (430,790), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        cv2.putText(frame, str(reps), (435,910), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 5, cv2.LINE_AA)
        
        # cv2.putText(frame, 'STATUS', (65,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame, status, (160,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        cv2.imshow('Training Censor', frame)
        # print(frame.shape) # 이미지 세로, 가로, channel


        if cv2.waitKey(1) == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()