from flask import Flask, jsonify,render_template, send_from_directory,Response
from robot.util.robotLight import RobotLight
import time,os
#from robot.vis.camera_pi import Camera
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

app = Flask(__name__)
dir_path=os.path.dirname(os.path.realpath(__file__));

RL=RobotLight();
RL.start()
#cap=cv2.VideoCapture(0);

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
'''
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
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        frame=detect_faces(frame);
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



# import the necessary packages
# initialize the camera and grab a reference to the raw camera capture

def cap_image():
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)
    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    return image


def cap_video():
# initialize the camera and grab a reference to the raw camera capture
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
        # show the frame
        cv2.imshow("Frame", image)
#        time.sleep(0.1)
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break


def main():
    cap_video();
    s=input("pause");
    image=cap_image();
    # display the image on screen and wait for a keypress
    cv2.imshow("Image", image)
    cv2.waitKey(0)


if(__name__=="__main__"):
    main();
