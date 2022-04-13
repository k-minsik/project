import cv2
import mediapipe as mp
import pymysql
import count
import sqldef


# conn = pymysql.connect(host='localhost', user='root', password='alstlr2!', db='mbt1', charset='utf8mb4')
# cursor = conn.cursor()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('squat.mp4')
    def __del__(self):
        self.video.release()
    def get_frame(self, reps, status):
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            success, frame = self.video.read()

            # To improve performance, optionally mark the frame as not writeable to
            # pass by reference.
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame)

            # Draw the pose annotation on the frame.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            frame = cv2.flip(frame, 1)
            # print(frame.shape) # 이미지 세로, 가로, channel
            height, width, _ = frame.shape

            cv2.rectangle(frame, (width-width//3,height-height//3), (width,height), (255,255,255), -1)
            cv2.putText(frame, 'REPS', (int(width-width//3.1),int(height-height//3.6)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
            cv2.putText(frame, str(reps), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 4, cv2.LINE_AA)
            cv2.putText(frame, status, (0,int(height//10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            frame = cv2.flip(frame, 1)

            try:
                landmarks = results.pose_landmarks.landmark
                # print(landmarks)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                rightToe = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
                leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                leftToe = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                
                kneeAngle = (count.get_angle(rightHip, rightKnee, rightAnkle) + count.get_angle(leftHip, leftKnee, leftAnkle)) / 2
                hipAngle = (count.get_angle(rightShoulder, rightHip, rightKnee) + count.get_angle(leftShoulder, leftHip, leftKnee)) / 2
                ankleAngle = (count.get_angle(rightKnee, rightAnkle, rightToe) + count.get_angle(leftKnee, leftAnkle, leftToe)) / 2
                elbowAngle = (count.get_angle(rightShoulder, rightElbow, rightWrist) + count.get_angle(leftShoulder, leftElbow, leftWrist)) / 2

                #Squat
                reps, status = count.squat(hipAngle, kneeAngle, ankleAngle, reps, status)
                # reps = count.just_test(reps)
                # print(reps)

                # try:
                #     sqldef.saveData(cursor, conn, "sqaut", reps)
                #     print("성공")
                # except:
                #     print("실패")

                # r1rm = count.onerm(weight, reps) #나중엔 바꿔야 할거 같음

                #BenchPress
                # elbowAngle, reps, status = count.benchpress(elbowAngle, reps, status)

                #DeadLift
                # hipAngle, kneeAngle, reps, status = count.deadlift(hipAngle, kneeAngle, reps, status)

            except:
                pass

            frame = cv2.flip(frame, 1)
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes(), reps, status



# def measurement():
#     global reps
#     reps = 0
#     status = "start"

#     # camera = cv2.VideoCapture(0)
#     camera = cv2.VideoCapture('squat.mp4')
#     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         while True:
#             success, frame = camera.read()
#             if not success:
#                 continue

#             # To improve performance, optionally mark the frame as not writeable to
#             # pass by reference.
#             frame.flags.writeable = False
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = pose.process(frame)

#             # Draw the pose annotation on the frame.
#             frame.flags.writeable = True
#             frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

#             frame = cv2.flip(frame, 1)
#             # print(frame.shape) # 이미지 세로, 가로, channel
#             height, width, _ = frame.shape

#             cv2.rectangle(frame, (width-width//3,height-height//3), (width,height), (255,255,255), -1)
#             cv2.putText(frame, 'REPS', (int(width-width//3.1),int(height-height//3.6)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
#             cv2.putText(frame, str(reps), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 4, cv2.LINE_AA)
#             cv2.putText(frame, status, (0,int(height//10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
#             frame = cv2.flip(frame, 1)

#             try:
#                 landmarks = results.pose_landmarks.landmark
#                 # print(landmarks)
#                 mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

#                 rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
#                 rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
#                 rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
#                 rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
#                 rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
#                 rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
#                 rightToe = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
#                 leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#                 leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
#                 leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
#                 leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
#                 leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
#                 leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
#                 leftToe = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                
#                 kneeAngle = (count.get_angle(rightHip, rightKnee, rightAnkle) + count.get_angle(leftHip, leftKnee, leftAnkle)) / 2
#                 hipAngle = (count.get_angle(rightShoulder, rightHip, rightKnee) + count.get_angle(leftShoulder, leftHip, leftKnee)) / 2
#                 ankleAngle = (count.get_angle(rightKnee, rightAnkle, rightToe) + count.get_angle(leftKnee, leftAnkle, leftToe)) / 2
#                 elbowAngle = (count.get_angle(rightShoulder, rightElbow, rightWrist) + count.get_angle(leftShoulder, leftElbow, leftWrist)) / 2

#                 #Squat
#                 reps, status = count.squat(hipAngle, kneeAngle, ankleAngle, reps, status)

#                 try:
#                     sqldef.saveData(cursor, conn, "sqaut", reps)
#                     print("성공")
#                 except:
#                     print("실패")

#                 # r1rm = count.onerm(weight, reps) #나중엔 바꿔야 할거 같음

#                 #BenchPress
#                 # elbowAngle, reps, status = count.benchpress(elbowAngle, reps, status)

#                 #DeadLift
#                 # hipAngle, kneeAngle, reps, status = count.deadlift(hipAngle, kneeAngle, reps, status)

#             except:
#                 pass

#             frame = cv2.flip(frame, 1)
#             _, buffer = cv2.imencode('.jpg', frame)
#             return buffer.tobytes()