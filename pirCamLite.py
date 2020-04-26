from Pubnub import Pubnub
from detector import Detector
import RPi.GPIO as GPIO
import time
import picamera
import sys, os
import json,httplib
import base64

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

pubnub = Pubnub(publish_key = 'pub-c-f83b8b34-5dbc-4502-ac34-5073f2382d96',
                subscribe_key = 'sub-c-34be47b2-f776-11e4-b559-0619f8945a4f')

cam = picamera.PiCamera()

channel2 = 'liveCamClick'

startT = time.time()
# count = 0

channel = 'iotchannel'
message = "hello from pi"
 
# imgCount = 5

def _callback(msg, n):
    print(msg)
    curTime = (time.strftime("%I:%M:%S")) + ".jpg"
    cam.capture(curTime, resize=(320,240))
    with open(curTime, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    connection.request('POST', '/1/classes/Selfie', json.dumps({
        "fileData": encoded_string,
        "fileName": curTime,
    }), {
        "X-Parse-Application-Id": "S7cS6MQyMb7eMjWRWsC32owq9cDx0zyrM58MSevK",
        "X-Parse-REST-API-Key": "RghYdl6Z2Pqpl2KjIqacZE6AoRn4csLM02e6j6ZH",
        "Content-Type": "application/json"
    })
    try:
        result = json.loads(connection.getresponse().read())
        print result
    except:
        print "Error Uploading."
    pubnub.publish(channel,curTime)
    os.remove(curTime)


def _error(m):
        print(m)

# def is_person(image):
#     det = Detector(image)
#     return len(det.face()) or len(det.upper_body()) or len(det.pedestrian())

try:
    cam.start_preview()
    cam.preview_fullscreen = False
    cam.preview_window = (10,10, 320,240)

    pubnub.subscribe(channels=channel2, callback=_callback, error=_error)
    # Listening for messages on the channel
    while True:
        time.sleep(10)

    

except KeyboardInterrupt:
  cam.stop_preview()
  sys.exit(0)