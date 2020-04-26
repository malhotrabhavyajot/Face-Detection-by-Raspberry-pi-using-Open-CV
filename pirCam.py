from detector import Detector
import RPi.GPIO as GPIO
import time
import picamera
import sys, os
import json,httplib
import base64
import threading

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
previous_state = False
current_state = False
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
cam = picamera.PiCamera()
lock = threading.Lock()

channel    = 'iotchannel'
subchannel = 'liveCamStatus'
 
## Camera Settings
imgCount   = 3
frameSleep = 0.5    # Seconds between burst-snaps
camSleep   = 5      # Seconds between Detections

def _error(m):
    print(m)

def _kill(m, n):

def is_person(image):
    det = Detector(image)
    faces = len(det.face())
    print "FACE: ", det.drawColors[det.drawn-1 % len(det.drawColors)], faces
    uppers = len(det.upper_body())
    print "UPPR: ", det.drawColors[det.drawn-1 % len(det.drawColors)], uppers
    fulls = len(det.full_body())
    print "FULL: ", det.drawColors[det.drawn-1 % len(det.drawColors)], fulls
    peds = len(det.pedestrian())
    print "PEDS: ", det.drawColors[det.drawn-1 % len(det.drawColors)], peds
    det.draw()
    det.overlay()
   
    return faces + uppers + fulls + peds
    # return len(det.face()) or len(det.full_body()) or len(det.upper_body()) # or len(det.pedestrian())

def processImage(imgFile):
    global connection
    if is_person(imgFile):
        print "True"
        with open(imgFile, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        lock.acquire()
        try:
            connection.request('POST', '/1/classes/Selfie', json.dumps({
                "fileData": encoded_string,
                "fileName": imgFile,
            }), {
                "X-Parse-Application-Id": "S7cS6MQyMb7eMjWRWsC32owq9cDx0zyrM58MSevK",
                "X-Parse-REST-API-Key": "RghYdl6Z2Pqpl2KjIqacZE6AoRn4csLM02e6j6ZH",
                "Content-Type": "application/json"
            })
            result = json.loads(connection.getresponse().read())
            print "Photo Uploaded!"
        except:
            connection.close()
            connection = httplib.HTTPSConnection('api.parse.com', 443)
            connection.connect()
            print "Error Uploading."
        lock.release()
    else:   # Not a person
        print "False"
    os.remove(imgFile)
    sys.exit(0) 

try:
   
    while True:
        previous_state = current_state
        current_state = GPIO.input(sensor)
        if current_state != previous_state:
            new_state = "HIGH" if current_state else "LOW"
            if current_state:     # Motion is Detected
                lock.acquire()
                cam.start_preview() # Comment in future
                cam.preview_fullscreen = False
                cam.preview_window = (10,10, 320,240)
                print('Motion Detected')
                
                for i in range(imgCount):
                    curTime = (time.strftime("%I:%M:%S")) + ".jpg"
                    cam.capture(curTime, resize=(320,240))
                    t = threading.Thread(target=processImage, args = (curTime,))
                    t.daemon = True
                    t.start()
                    time.sleep(frameSleep)
                cam.stop_preview()
                lock.release()
                time.sleep(camSleep)

except KeyboardInterrupt:
  cam.stop_preview()
  sys.exit(0)
