from keras.preprocessing.image import img_to_array
import imutils
import cv2
import time
from keras.models import load_model
import numpy as np
import threading
from common.const import *


class emotionHijacker:
    def __init__(self):
        # parameters for loading data and images
        detection_model_path = 'emotion_recognition/haarcascade_files/haarcascade_frontalface_default.xml'
        emotion_model_path = 'emotion_recognition/models/_mini_XCEPTION.102-0.66.hdf5'

        # hyper-parameters for bounding boxes shape
        # loading models
        self.face_detection = cv2.CascadeClassifier(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        self.EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

        self.emo = 4
        self.done = False
        self.canvas = None
        self.frame_clone = None

    def ready(self):
        self.camera = cv2.VideoCapture(0)
        self.t = threading.Thread(target=self._hijack)
        self.t.start()
        time.sleep(1)

    def hijack(self):
        return self.emo

    def get_frame(self):
        return self.canvas, self.frame_clone

    def _hijack(self):
        while not self.done:
            # starting video streaming
            frame = self.camera.read()[1]
            # reading the frame
            frame = imutils.resize(frame, height=int(SIZE[1] * 0.6))  # size of video
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                    flags=cv2.CASCADE_SCALE_IMAGE)

            self.canvas = np.zeros((250, 300, 3), dtype="uint8")
            self.frame_clone = frame.copy()
            if len(faces) > 0:
                faces = sorted(faces, reverse=True,
                               key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
                (fX, fY, fW, fH) = faces
                # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
                # the ROI for classification via the CNN
                roi = gray[fY:fY + fH, fX:fX + fW]
                roi = cv2.resize(roi, (64, 64))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                preds = self.emotion_classifier.predict(roi)[0]
                emotion_probability = np.max(preds)
                label = self.EMOTIONS[preds.argmax()]
            else:
                continue

            for (i, (emotion, prob)) in enumerate(zip(self.EMOTIONS, preds)):
                # construct the label text
                text = "{}: {:.2f}%".format(emotion, prob * 100)

                # draw the label + probability bar on the canvas
                # emoji_face = feelings_faces[np.argmax(preds)]

                w = int(prob * 300)
                cv2.rectangle(self.canvas, (7, (i * 35) + 5),
                              (w, (i * 35) + 35), (0, 0, 255), -1)
                cv2.putText(self.canvas, text, (10, (i * 35) + 23),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (255, 255, 255), 2)
                # cv2.putText(self.frame_clone, label, (fX, fY - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                cv2.rectangle(self.frame_clone, (fX, fY), (fX + fW, fY + fH),
                              (0, 0, 255), 2)
            #    for c in range(0, 3):
            #        frame[200:320, 10:130, c] = emoji_face[:, :, c] * \
            #        (emoji_face[:, :, 3] / 255.0) + frame[200:320,
            #        10:130, c] * (1.0 - emoji_face[:, :, 3] / 255.0)

            # cv2.imshow('your_face', frameClone)
            # cv2.imshow("Probabilities", self.canvas)

            # ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
            emo = preds.argmax()

            if emo == 0:
                emo = 2
            elif emo == 3:
                emo = 1
            elif emo == 5:
                emo = 3
            elif emo == 6:
                emo = 0
            else:
                emo = 4

            self.emo = emo

    def terminate(self):
        self.done = True
        self.t.join()
        self.camera.release()
        cv2.destroyAllWindows()
