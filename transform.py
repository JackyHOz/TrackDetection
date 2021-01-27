import cv2
import numpy as np
#Read Image
img = cv2.imread('image0.jpg')
#Coordination test
#cv2.circle(img,(595,430),5,(0,0,255),-1)
#cv2.circle(img,(1515,420),5,(0,0,255),-1)
#cv2.circle(img,(285,565),5,(0,0,255),-1)
#cv2.circle(img,(1880,555),5,(0,0,255),-1)

#Define transformation coordinates
con1 = np.float32([[595,430],[1515,420],[-1000,1100],[2900,1100]])
con2 = np.float32([[0,0],[1880,0],[0,565],[1880,565]])
#Transform
matrix = cv2.getPerspectiveTransform(con1,con2)
result = cv2.warpPerspective(img,matrix,(1880,565))

#Test Phrase
imgGray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
imgThreshold = cv2.Canny(imgBlur, 240, 240)
kernel = np.ones((5,5))
imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)
imgThreshold = cv2.erode(imgDial, kernel, iterations=1)
imgContours = result.copy()
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 5)


#Output Image
cv2.imwrite('marked.jpg', img)
cv2.imwrite('fin.jpg', result)
cv2.imwrite('processed.jpg', imgContours)