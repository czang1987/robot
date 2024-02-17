from flask import Flask, jsonify,render_template, send_from_directory,Response
from robot.util.robotLight import RobotLight
import time,os
#from robot.vis.camera_pi import Camera
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from robot.util import  ultra
from robot.robot_car import RobotCar

car=RobotCar()

app = Flask(__name__)
dir_path=os.path.dirname(os.path.realpath(__file__));

#RL=RobotLight();
#RL.start()
#cap=cv2.VideoCapture(0);

@app.route('/move_backward_function', methods=['GET'])
def move_backward_function():
    # Your Python function logic goes here
#    RL.breath(70,70,255)
    car.test("move_backward")
    result = {'message': 'move backward called successfully'}
    return jsonify(result)

@app.route('/turn_left_function', methods=['GET'])
def turn_left_function():
    # Your Python function logic goes here
#    RL.breath(70,70,255)
    car.test("turn_left")
    result = {'message': 'turn left called successfully'}
    return jsonify(result)

@app.route('/turn_right_function', methods=['GET'])
def turn_right_function():
    # Your Python function logic goes here
#    RL.breath(70,70,255)
    car.test("turn_right")
    result = {'message': 'turn right called successfully'}
    return jsonify(result)

@app.route('/move_forward_function', methods=['GET'])
def move_forward_function():
    # Your Python function logic goes here
#    RL.breath(70,70,255)
    car.test("move_forward")
    result = {'message': 'move forward called successfully'}
    return jsonify(result)

@app.route('/motor_stop_function', methods=['GET'])
def motor_stop_function():
    # Your Python function logic goes here
#    RL.breath(70,70,255)
    car.test("stop")
    result = {'message': 'motor stop called successfully'}
    return jsonify(result)

@app.route('/start_light_function', methods=['GET'])
def start_light_function():
    # Your Python function logic goes here
#    RL.breath(70,70,255)
    car.test("breath_on")
    result = {'message': 'start light called successfully'}
    return jsonify(result)

@app.route('/end_light_function', methods=['GET'])
def end_light_function():
    # Your Python function logic goes here
    car.test("light_off")
#    RL.pause();
    result = {'message': 'end light called successfully'}
    return jsonify(result)
'''
def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        frame_with_faces=detect_faces(frame)
        ret,buffer=cv2.imencode('.jpg',frame_with_faces)
        frame=buffer.tobytes();

        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'
'''

def cap_video():
# initialize the camera and grab a reference to the raw camera capture
    """Video streaming generator function."""
    yield b'--frame\r\n'
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # allow the camera to warmup
    time.sleep(0.1)
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        #show distance
        dist_str="%.2f"%ultra.checkdist()
        image = cv2.putText(image,dist_str,(50,50),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,0,0),2,cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()

#        frame=detect_faces(frame);
        rawCapture.truncate(0)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(cap_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/js/<path:filename>')
def sendjs(filename):
    return send_from_directory(dir_path+'/template/js', filename)


if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)



