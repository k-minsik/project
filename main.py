import cv2
import mediapipe as mp
from flask import Flask, render_template, Response
import count

app = Flask(__name__)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


# camera = cv2.VideoCapture('squat.mp4')
camera = cv2.VideoCapture(0)

def gen_frames():  
    reps = 0 
    status = "Start"

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            success, frame = camera.read()
            if not success:
                continue

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
                print(landmarks)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

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

                # Flip the frame horizontally for a selfie-view display.
                
            except:
                pass

            frame = cv2.flip(frame, 1)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)