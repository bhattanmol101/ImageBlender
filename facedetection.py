from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2
import os


def getBlendedImage():
    directory = os.fsencode('./img')
    imgArray = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
            imgArray.append(filename)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        "./model/shape_predictor_68_face_landmarks.dat")
    fa = FaceAligner(predictor, desiredFaceWidth=256)

    image1 = cv2.imread("./img/" + imgArray[0])
    image1 = imutils.resize(image1, width=1000)
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    rects1 = detector(gray1, 2)
    image2 = cv2.imread("./img/" + imgArray[1])
    image2 = imutils.resize(image2, width=1000)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    rects2 = detector(gray2, 2)

    for rect in rects1:
        (x, y, w, h) = rect_to_bb(rect)
        faceOrig = imutils.resize(image1[y:y + h, x:x + w])
        faceAligned1 = fa.align(image1, gray1, rect)

    for rect in rects2:
        (x, y, w, h) = rect_to_bb(rect)
        faceOrig = imutils.resize(image2[y:y + h, x:x + w])
        faceAligned2 = fa.align(image2, gray2, rect)

    img_blend = cv2.addWeighted(faceAligned1, 0.5, faceAligned2, 0.5, 0.0)
    if not os.path.isdir("./merged"):
        os.makedirs("./merged")
    elif os.path.isfile("./merged/pic.png"):
        os.remove("./merged/pic.png")
    cv2.imwrite("./merged/pic.png", img_blend)
