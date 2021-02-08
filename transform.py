import cv2
import numpy as np
import os
import fnmatch

def transformationimages(image):
    #Read Image
    img = cv2.imread('./tracktest2/'+image)

    #Define transformation coordinates
    con1 = np.float32([[595,430],[1515,420],[-1000,1100],[2900,1100]])
    con2 = np.float32([[0,0],[1880,0],[0,565],[1880,565]])

    #Transform
    matrix = cv2.getPerspectiveTransform(con1,con2)
    result = cv2.warpPerspective(img,matrix,(1880,565))

    #Test Phrase
    kernel_sharp = np.array([[0, -1, 0],
                            [-1, 5,-1],
                            [0, -1, 0]])
    imgSharp = cv2.filter2D(result, -1, kernel_sharp)
    imgGray = cv2.cvtColor(imgSharp, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgThreshold = cv2.Canny(imgBlur, 250, 250)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)
    imgContours = imgSharp.copy()
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 5)

    #Output Image
    cv2.imwrite(image, result)
    cv2.imwrite(image, imgContours)
    cv2.imwrite(image, imgSharp)

def main():
    for dirPath, dirNames, fileNames in os.walk('./tracktest2'):
        # print(fileNames)
        for picture in fnmatch.filter(fileNames, '*.jpg'):
            # print(picture)
            transformationimages(picture)

if __name__ == "__main__":
    main()
