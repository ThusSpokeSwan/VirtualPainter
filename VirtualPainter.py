import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

# Settings for brush and eraser thickness
brushThickness = 15
eraserThickness = 80

# Load header images
folderPath = 'Header'
myList = os.listdir(folderPath)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]
drawColor = (255, 0, 255) #default drawing color

# Initialize webcam and hand detector
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.HandDetector(detectionCon=0.85)
xp,yp = 0,0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # Import and Flip the image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detect hands and positions
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    mode = "" # Variable to store the current mode for on-screen feedback

    if len(lmList) != 0:
        # tip of index & middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Which fingers are up
        fingers = detector.fingersUp()


        # Selection mode = Both index and middle fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0 # Reset previous positions
            mode = "Selection Mode"

            # Modify header
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 13), (x2, y2 + 13), drawColor, cv2.FILLED)


        # Drawing mode = Only index finger is up
        elif fingers[1] and not fingers[2]:
            # Set mode text based on selected tool
            if drawColor == (0, 0, 0):
                mode = "Eraser Mode"
            else:
                mode = "Drawing Mode"

            cv2.circle(img, (x1, y1), 7, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Draw on canvas and the image
            if drawColor == (0, 0, 0): # Eraser mode
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    # Overlay the current mode on the image
    cv2.putText(img, mode, (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

    # Creating inverted mask of the canvas and blending it with the image
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header
    img[0:125, 0:1280] = header

    cv2.imshow("Image", img)
    cv2.waitKey(1)