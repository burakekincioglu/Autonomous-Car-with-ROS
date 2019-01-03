import cv2
import imutils
import numpy as np
import rospy
from std_msgs.msg import String

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
            # if the shape has 4 vertices, it is either a square or
            # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.93 and ar <= 1.07 else "rectangle"

            # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

            # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

            # return the name of the shape

        return shape

cap = cv2.VideoCapture(1)


pub = rospy.Publisher("durak", String, queue_size = 10)
rospy.init_node('durak', anonymous=True)
rate = rospy.Rate(1) # 10hz
counter = 0
while True:
    counter += 1
    if counter % 5 == 0:

    # Capture frame-by-frame
        #ret, frame = cap.read()
        ret,frame = cap.read()
        frame = frame[0:240,400:]
        # convert the resized image to grayscale, blur it slightly,
        # and threshold it
        shape = None
        lower_blue = np.array([70,0,0])
        upper_blue = np.array([150,40,30])
        mask = cv2.inRange(frame, lower_blue, upper_blue);
        mavi = cv2.bitwise_and(frame,frame, mask= mask)
        gray = cv2.cvtColor(mavi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 16, 255, cv2.THRESH_BINARY)[1]

        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        for c in cnts:
    	# compute the center of the contour, then detect the name of the
    	# shape using only the contour
        	M = cv2.moments(c)
        	cX = int((M["m10"] / (M["m00"]+1e-7)) )
        	cY = int((M["m01"] / (M["m00"]+1e-7)) )
            	sd = ShapeDetector()
        	shape = sd.detect(c)
            #print "SHAPE: " +str(shape)

        	# multiply the contour (x, y)-coordinates by the resize ratio,
        	# then draw the contours and the name of the shape on the image
        	c = c.astype("int")
        	cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        	cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        		0.5, (255, 255, 255), 2)

        	# show the output image
        #cv2.imshow("gray",gray)
        #cv2.imshow("mavi",mavi)
        #cv2.imshow("thresh",thresh)
        #cv2.imshow("frame",frame)
        if shape == "square":
            msg = String()
            msg.data = "durak"
            pub.publish(msg)
            rate.sleep()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        counter = counter % 5
        """subDurak  =  rospy.Subscriber("durak", String, callback)
        rospy.spin()
        def callback(msg):
            if msg=="durak":
                
        """
