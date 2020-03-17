import numpy as np
import argparse
import cv2
import imutils
import serial
from threading import Thread
from statistics import mean
#ser = serial.Serial('COM10',115200)
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""

    def __init__(self, resolution=(640, 480), framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

        # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
        # Start the thread that reads frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Return the most recent frame
        return self.frame

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True


cap = VideoStream(resolution=(1280, 720), framerate=30).start()

print("camera found")

#cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
#if not (cap.isOpened()):
#    print("Could not open video device")

#cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)

#cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

#image = cv2.imread("color_detection_red_version.jpg")
boundaries = [
    ([36, 0, 0] , [ 86, 255, 255])
    #([131, 190, 137], [74, 148, 100])
]

def center_find():
    samples = []
    while True:
        image = cap.read()
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY)[1]
        """
        for (lower, upper) in boundaries:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(image, lower, upper)
            output = cv2.bitwise_and(image, image, mask = mask)
            # show the images

        #cv2.imshow("images",output)
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in cnts]
        M = []
        try:
            c = max(contour_sizes, key=lambda x: x[0])[1]
            M = cv2.moments(c)
        except ValueError:
            pass
        #for c in cnts:
            # compute the center of the contour
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # draw the contour and center of the shape on the image
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(image, "center", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            samples += [[cX, cY]]
            # show the image
        except (ZeroDivisionError, TypeError) as e:
                pass
        cv2.imshow("Image", image)

    return
