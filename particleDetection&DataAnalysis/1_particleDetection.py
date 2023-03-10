import cv2 as cv
import numpy as np

def frameResize(frame, scale=0.75):
    width       = int(frame.shape[1]*scale)
    height      = int(frame.shape[0]*scale)
    dimensions  = (widht, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img         = cv.imread("C:\\Users\\sahil\\Documents\\MA202-project\\mathsProject(MA202)\\images\\Img_00353.tif")

imgCopy     = img.copy()

gray        = cv.cvtColor(imgCopy, cv.COLOR_BGR2GRAY)

blur        = cv.GaussianBlur(gray, (19, 19), 0)

threshold   = cv.threshold(blur, 125, 255, cv.THRESH_BINARY)[1]

circles     = cv.HoughCircles(threshold, cv.HOUGH_GRADIENT, 2.8, 13, param1 = 20, param2 = 10, minRadius = 1, maxRadius = 7)

print(circles)  #3D array (each image, total particles, coordinates&radius) 

circles_data = np.uint16(np.around(circles))

ct = 0
for (x, y, r) in circles_data[0, :] :
    cv.circle(imgCopy, (x, y), r, (0, 255, 0), 2)
    cv.circle(imgCopy, (x, y), 1, (0, 255, 0), 2)
    ct = ct + 1

imgCopy = frameResize(imgCopy)
gray = frameResize(gray)
blur = frameResize(blur)
threshold = frameResize(threshold)
img = frameResize(img)

cv.imshow("Original image", img)
cv.imshow("Blur image", blur)
cv.imshow("Grayscale image", gray)
cv.imshow("Thresholded image", threshold)
cv.imshow("Detected Circles", imgCopy)

print(ct)

cv.waitKey(0)