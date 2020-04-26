import cv2
import sys
import random
import numpy as np
import datetime
import random

class Detector():
	def __init__(self, image):
		self.image_name = image
		self.image = []
		self.drawn = 0
		self.drawColors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
		# self.path  = "/home/pi/CV/opencv-2.4.10/data/haarcascades/"
		self.path = "xml/"
		self.rects = []
		self.overlays = ["face","obama","lebron","curry", "nick", 
						"bat", "captain", "hulk", "ironman", "spider","xmen"]

	def detect(self, xml):
		cascade = cv2.CascadeClassifier(self.path + xml)
		self.image = cv2.imread(self.image_name)
		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		hits = cascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(10, 10),
			flags=cv2.CASCADE_SCALE_IMAGE
		)
		self.rects.append(hits)
		return hits

	def face(self):
		return self.detect('haarcascade_frontalface_default.xml')

	def face2(self):
		return self.detect('haarcascade_frontalface_alt.xml')

	def face3(self):
		return self.detect('haarcascade_frontalface_alt2.xml')

	def full_body(self):
		return self.detect('haarcascade_fullbody.xml')

	def upper_body(self):
		return self.detect('haarcascade_upperbody.xml')

	#def pedestrian(self):
		#return self.detect("hogcascade_pedestrians.xml")

	def draw(self):
		for hits in self.rects:
			color = self.drawColors[self.drawn % len(self.drawColors)]
			self.drawn += 1
			for (x,y,w,h) in hits:
				cv2.rectangle(self.image, (x, y), (x+w, y+h), color, 5)
		cv2.imwrite(self.image_name, self.image)
		cv2.imshow('image',self.image)
		cv2.waitKey(0)
		return hits
		
	def log(self):
	    f1 = open("log.txt", "w+")
        '''txt = datetime.datetime.now()
        f1.write(txt)'''

	def overlay(self):
		for (x,y,w,h) in self.rects[0]:
			img_offset = 30
			x_offset = x
			y_offset = y - img_offset/2
			img = random.choice(self.overlays)
			s_img = cv2.imread("Overlay/"+img+".png", -1)
			s_img = cv2.resize(s_img, (w,h+img_offset))
			for c in range(0,3):
			    self.image[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1], c] =  \
			    s_img[:,:,c] * (s_img[:,:,3]/255.0) +  self.image[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1], c] * (1.0 - s_img[:,:,3]/255.0)
			cv2.imwrite(self.image_name, self.image)
			#resized_image = cv2.resize(self.image, (600, 600)) 
			#cv2.imshow('image', resized_image)
			#cv2.waitKey(0)
			# cv2.destroyAllWindows()

## Test
# det = Detector("img_5.jpg")
# print det.pedestrian()


cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    '''if cv2.waitKey(1) and 0xFF == ord('z'):
		
		break'''

    if cv2.waitKey(1) & 0xFF == ord('z'):
	raand = random.randrange(20,50,3)
        cv2.imwrite("database/x"+str(raand)+".jpg",frame)
        det = Detector("database/x" + str(raand) + ".jpg")
	print "MOTION DETECTED"
        faces = len(det.face())
        print "FACE: ", det.drawColors[det.drawn-1 % len(det.drawColors)], faces
        uppers = len(det.upper_body())
        print "UPPR: ", det.drawColors[det.drawn-1 % len(det.drawColors)], uppers
        fulls = len(det.full_body())
        print "FULL: ", det.drawColors[det.drawn-1 % len(det.drawColors)], fulls
        #peds = len(det.pedestrian())
        #print "PEDS: ", det.drawColors[det.drawn-1 % len(det.drawColors)], peds
        det.draw()
        #det.overlay()
        print datetime.datetime.now()
        print fulls
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
