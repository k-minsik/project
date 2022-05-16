import cv2
import mediapipe as mp
from flask import Flask, jsonify, render_template, Response, request
import pymysql
import count
import sqldef


conn = pymysql.connect(host='localhost', user='root', password='', db='mbt1', charset='utf8mb4')
cursor = conn.cursor()

app = Flask(__name__)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

reps_s = 0
reps_b = 0
reps_d = 0

# url = 'http://172.30.1.7:8000/'


def gen_frames(event):
    global reps_s, reps_b, reps_d
    side = 0
    status = "start"

    # camera = cv2.VideoCapture(1)
    # camera = cv2.VideoCapture(url)
    if event == "Squat":
        reps_s = 0
        camera = cv2.VideoCapture('squat2.mp4')
        # camera = cv2.VideoCapture(0)
    elif event == "BenchPress":
        reps_b = 0
        camera = cv2.VideoCapture('bench.mp4')
        # camera = cv2.VideoCapture(0)
    elif event == "Deadlift":
        reps_d
        camera = cv2.VideoCapture('dead.mp4')
        # camera = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            success, frame = camera.read()
            if not success:
                continue

            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame)

            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # print(frame.shape) # 이미지 세로, 가로, channel
            height, width, _ = frame.shape

            cv2.rectangle(frame, (width-width//3,height-height//3), (width,height), (255,255,255), -1)
            cv2.putText(frame, 'REPS', (int(width-width//3.1),int(height-height//3.6)), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0,0,0), 2, cv2.LINE_AA)
            if event == "Squat":
                cv2.putText(frame, str(reps_s), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,0), 4, cv2.LINE_AA)
            elif event == "BenchPress":
                cv2.putText(frame, str(reps_b), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,0), 4, cv2.LINE_AA)
            elif event == "Deadlift":
                cv2.putText(frame, str(reps_d), (int(width-width//4),int(height-height//9)), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,0), 4, cv2.LINE_AA)
            
            cv2.putText(frame, status, (0,int(height//10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            try:
                landmarks = results.pose_landmarks.landmark
                # print(landmarks)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                rightToe = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
                rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                leftToe = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                RkneeAngle = count.get_angle(rightHip, rightKnee, rightAnkle)
                RhipAngle = count.get_angle(rightShoulder, rightHip, rightKnee)
                RankleAngle = count.get_angle(rightKnee, rightAnkle, rightToe)
                RelbowAngle = count.get_angle(rightShoulder, rightElbow, rightWrist)

                LelbowAngle = count.get_angle(leftShoulder, leftElbow, leftWrist)
                LkneeAngle = count.get_angle(leftHip, leftKnee, leftAnkle)
                LhipAngle = count.get_angle(leftShoulder, leftHip, leftKnee)
                LankleAngle = count.get_angle(leftKnee, leftAnkle, leftToe)

                if event == "Squat":
                    #Squat
                    reps_s, status, side = count.squat(RhipAngle, RkneeAngle, RankleAngle, LhipAngle, LkneeAngle, LankleAngle, reps_s, status, side)
                elif event == "BenchPress":
                    #BenchPress
                    reps_b, status, side = count.benchpress(RelbowAngle, LelbowAngle, reps_b, status, side)
                elif event == "Deadlift":
                    #DeadLift
                    reps_d, status, side = count.deadlift(RhipAngle, RkneeAngle, LhipAngle, LkneeAngle, reps_d, status, side)
                
            except:
                pass

            resize_frame = cv2.resize(frame, (390, 520), interpolation=cv2.INTER_CUBIC)
            _, buffer = cv2.imencode('.jpg', resize_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Squat')
def video_feed_s():
    return Response(gen_frames("Squat"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/BenchPress')
def video_feed_b():
    return Response(gen_frames("BenchPress"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/Deadlift')
def video_feed_d():
    return Response(gen_frames("Deadlift"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reps/Squat', methods=['GET'])
def cnt_squat():
    return jsonify(data = reps_s)

@app.route('/reps/BenchPress', methods=['GET'])
def cnt_bench():
    return jsonify(data = reps_b)

@app.route('/reps/Deadlift', methods=['GET'])
def cnt_dead():
    return jsonify(data = reps_d)

@app.route('/result', methods=['POST'])
def result():
    params = request.get_json()
    sqldef.saveData(cursor, conn, params['event'], params['weight'], params['reps'], params['oneRM'])
    return params

@app.route('/profile/Total', methods=['GET'])
def userData_T():
    return jsonify(data = sqldef.getData(cursor, conn, "Total"))

@app.route('/profile/Squat', methods=['GET'])
def userData_S():
    return jsonify(data = sqldef.getData(cursor, conn, "Squat"))

@app.route('/profile/BenchPress', methods=['GET'])
def userData_B():
    return jsonify(data = sqldef.getData(cursor, conn, "BenchPress"))

@app.route('/profile/Deadlift', methods=['GET'])
def userData_D():
    return jsonify(data = sqldef.getData(cursor, conn, "Deadlift"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)