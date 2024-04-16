import cv2
import os
import numpy as np
import fitz
from cvzone.HandTrackingModule import HandDetector


def main():
    # Variables
    width, height = 1400, 800

    # Construct the path to the PDF file dynamically
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'AI_Examples_Module3.pdf')

    # Convert PDF to images
    doc = fitz.open(pdf_path)
    images = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
        # Ensure that the color space is BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        images.append(img)

    # Camera Setup
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    # Variables
    imgNumber = 0
    hs, ws = int(120 * 1.5), int(213 * 1.5)
    gestureThreshold = 400
    buttonPressed = False
    buttonCounter = 0
    buttonDelay = 30
    annotations = [[]]
    annotationNumber = 0
    annotationStart = False

    # Hand Detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    while True:
        # Importing Images
        success, webcam_img = cap.read()
        webcam_img = cv2.flip(webcam_img, 1)

        pdf_img = images[imgNumber].copy()

        hands, _ = detector.findHands(webcam_img)
        cv2.line(webcam_img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 4)

        if hands and not buttonPressed:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            cx, cy = hand['center']
            lmList = hand['lmList']

            # Constrain values for easier drawing
            xVal = int(np.interp(lmList[8][0], [width // 4, 3 * width // 4], [0, width]))
            yVal = int(np.interp(lmList[8][1], [height // 4, 3 * height // 4], [0, height]))
            indexFinger = xVal, yVal

            if cy <= gestureThreshold:  # if hand is at the height of the face
                annotationStart = False
                # Gesture 1 -Left
                if fingers == [1, 0, 0, 0, 0]:
                    annotationStart = False
                    # print("Left")
                    if imgNumber > 0:
                        buttonPressed = True
                        annotations = [[]]
                        annotationNumber = 0
                        imgNumber -= 1

                # Gesture 2 -Right
                if fingers == [0, 0, 0, 0, 1]:
                    annotationStart = False
                    # print("Right")
                    if imgNumber < len(images) - 1:
                        buttonPressed = True
                        annotations = [[]]
                        annotationNumber = 0
                        imgNumber += 1

            # Gesture 3 - Show Pointer
            if fingers == [0, 1, 1, 0, 0]:
                cv2.circle(pdf_img, indexFinger, 6, (0, 0, 255), cv2.FILLED)
                annotationStart = False

            # Gesture 4 - Drawing
            if fingers == [0, 1, 0, 0, 0]:
                if annotationStart is False:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])
                cv2.circle(pdf_img, indexFinger, 6, (0, 0, 255), cv2.FILLED)
                annotations[annotationNumber].append(indexFinger)
            else:
                annotationStart = False

            # Gesture 5 - Eraser
            if fingers == [0, 1, 1, 1, 1]:
                if annotations:
                    if annotationNumber >= 0:
                        annotations.pop(-1)
                        annotationNumber -= 1
                        buttonPressed = True
        else:
            annotationStart = False

        # Button Pressed
        if buttonPressed:
            buttonCounter += 1
            if buttonCounter > buttonDelay:
                buttonCounter = 0
                buttonPressed = False

        for i in range(len(annotations)):
            for j in range(len(annotations[i])):
                if j != 0:
                    cv2.line(pdf_img, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 4)

        # Resize images to fit within the laptop screen
        webcam_img_resized = cv2.resize(webcam_img, (width // 4, height // 4))
        pdf_img_resized = cv2.resize(pdf_img, (width, height), interpolation=cv2.INTER_AREA)

        # Put webcam image in the top right corner
        pdf_img_resized[0:height // 4, 3 * width // 4:] = webcam_img_resized

        cv2.imshow("PDF with Annotations", pdf_img_resized)

        key = cv2.waitKey(1)
        if key == 27:  # If ESC key is pressed
            print("Execution successful")
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
