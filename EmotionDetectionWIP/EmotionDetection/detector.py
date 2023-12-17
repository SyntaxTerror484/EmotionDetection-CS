from keras.models import load_model
import numpy as np
import cv2
from keras.utils import img_to_array
from keras.preprocessing import image
from PIL import ImageGrab
import sys


class Detector:
    def __init__(self, arg):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.prediction_model = load_model('model')
        self.age_model = load_model('age')

        self.emotion_labels = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Neutral', 5:'Sad', 6:'Surprise'}
        self.colors = {0:(0, 128, 255), 1:(246, 61, 252), 2:(246, 61, 252), 3:(0,255,90), 4:(204, 204, 204), 5:(237, 28, 63), 6:(252,238,33)}
        self.arg = arg

        if (arg == '-c'):
            self.capture = cv2.VideoCapture(0)

    def capture_video(self, time_offset):
        emotion_list = []
        age_avg, age_avg_angry = 0, 0
        c1, c2 = 0, 0

        t = 0
        while True:
            camera = True
            if (self.arg == '-c'):
                _, frame = self.capture.read()

            else:    
                camera = False
                frame = np.array(ImageGrab.grab(bbox=(40,300,1200,1000)))
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in face:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                roi = gray[y : y + h, x : x + w]
                roi = cv2.resize(roi, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi]) != 0:
                    roi_ = roi.astype('float')/255.0
                    roi_ = img_to_array(roi_)
                    roi_ = np.expand_dims(roi_, axis=0)

                    prediction = self.prediction_model.predict(roi_)[0]
                    emotion = self.emotion_labels[prediction.argmax()]
                    age = str(int(self.age_model.predict(roi_)))
                    label_pos = (x, y - 10)

                    if emotion.lower() != 'angry':
                        age_avg = age_avg + int(age)
                        c1 = c1 + 1

                    else:
                        age_avg_angry = age_avg_angry + int(age)
                        c2 = c2 + 1
                    
                    if t % time_offset == 0:
                        print("Recording")
                        print(time_offset)
                        emotion_list.append(emotion)

                    cv2.putText(frame, f'{emotion}, {age}', label_pos, cv2.FONT_HERSHEY_PLAIN, 2, self.colors[prediction.argmax()], 2)

                else:
                    pass
            
            t = t + 1
            print(t)

            if not camera:
                cv2.imshow('Detector', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            else:
                cv2.imshow('Detector', frame)

            if cv2.waitKey(1) == ord('Q'):
                break

        cv2.destroyAllWindows()

        try:
            return (emotion_list, age_avg//c1, age_avg_angry//c2)
        
        except Exception as E:
            return None