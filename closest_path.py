import cv2
import numpy as np
import math

current_location = "courseq2.jpg"

#load current location image
img_bgr = cv2.imread(current_location)

#calculate size of current location image
img_size = cv2.imread(current_location,0)

#grayscale current location image
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

#load template for image mactching
template = cv2.imread('temp2.jpg',0)

#take width and height of template
w,h = template.shape[::-1]

#find the center of the image.
frame_w,frame_h = img_size.shape[::-1]
center_x = frame_w / 2
center_y = frame_h /2

#find matches and filter with a threshold
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.73
loc = np.where( res >= threshold)

#set placeholder variables
#bestDistance = hypothesis of closest path match
bestDistance = 9999999.0
#x(y)_distance are lengths of triangle arms
x_distance = 0.0
y_distance = 0.0
#target_x(y) are pixel endpoints from center 
target_x = 0.0
target_y = 0.0

#check all matches for closest path intersection
for pt in zip(*loc[::-1]):
	x_distance = center_x - (pt[0]+(w/2))
	y_distance = center_y - (pt[1]+(w/2))
	#distance from current location to center of path match.
	hypothesis = math.sqrt((y_distance **2)+(x_distance **2))
	if (hypothesis < bestDistance):
		bestDistance = hypothesis
		#zero_x(y) are only for drawing rectangle, remove in production.
		zero_x = pt[0]
		zero_y = pt[1]
		target_x = pt[0]+(w/2)
		target_y = pt[1]+(h/2)
#these are only for analysis, remove in production.
cv2.line(img_bgr,(center_x,center_y),(int(target_x),int(target_y)),(0,255,0),3)
cv2.rectangle(img_bgr,(zero_x,zero_y),(zero_x +w,zero_y +h),(0,255,0),2)
cv2.imshow('detected',img_bgr)
#all print statements are only for analysis remove in production.
print("center X: %d " % center_x)
print("center Y: %d " % center_y)
print("target X: %d " % target_x)
print("target Y: %d " % target_y)
print("best distance: %.2f pixels " % bestDistance)
#this heading assumes that due north is start of unit circle. 
print("at a heading of: %.2f rad " % (math.atan2( (target_x - center_x),(center_y - target_y)  ))) 
cv2.waitKey(0)


