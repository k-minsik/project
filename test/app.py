from flask import Flask, render_template, Response
from test import VideoCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.js')

def gen(camera):
    reps = 0
    status = 'Start'
    while True:
        frame, reps, status = camera.get_frame(reps, status)
        # print(str(reps) + status)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True, use_reloader=False)