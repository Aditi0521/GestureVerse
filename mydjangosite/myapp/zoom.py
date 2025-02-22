import cv2
from cvzone.HandTrackingModule import HandDetector
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.9)
startDist = 0
scale = 0
cx, cy = 500, 500
lmList1 = []  # Initialize lmList1
lmList2 = []  # Initialize lmList2
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    img1 = cv2.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'img.png'))

    if len(hands) == 2:
        # print (detector.fingersUp (hands [0]), detector.fingersUp (hands [1]))
        if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and \
                detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:

            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            # point 8 is the tip of the index finger
            if startDist is 0:
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
                # length, info, img = detector.findDistance(hands[0], lmList2[8], img)
                startDist = length

        # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
        length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
        scale = int((length - startDist) // 2)
        cx, cy = info[4:]
        

    else:
        startDist = 0
    try:
        h1, w1, _ = img1.shape
        newH, newW = ((h1 + scale) // 2) * 2, ((w1 + scale) // 2) * 2
        img1 = cv2.resize(img1, (newW, newH))
        img[cy - newH // 2:cy + newH // 2, cx - newW // 2:cx + newW // 2] = img1
    except:
        pass

    key = cv2.waitKey(1)
    if key == 27:  # If ESC key is pressed
        print("Execution successful")
        break

    # img[10:260, 18:268] = img1
    cv2.imshow("Image", img)
    cv2.waitKey(1)
