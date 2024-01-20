from flask import Flask, jsonify,render_template, send_from_directory,Response
from robot.util.robotLight import RobotLight
import time,os
from robot.vis.camera_pi import Camera

app = Flask(__name__)
dir_path=os.path.dirname(os.path.realpath(__file__));

RL=RobotLight();
RL.start()

@app.route('/start_light_function', methods=['GET'])
def start_light_function():
    # Your Python function logic goes here
    RL.breath(70,70,255)
    result = {'message': 'start light called successfully'}
    return jsonify(result)

@app.route('/end_light_function', methods=['GET'])
def end_light_function():
    # Your Python function logic goes here
    RL.pause();
    result = {'message': 'end light called successfully'}
    return jsonify(result)

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/js/<path:filename>')
def sendjs(filename):
    return send_from_directory(dir_path+'/template/js', filename)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)




