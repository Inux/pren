
import cv2
import imutils
import numpy as np
from keras.models import model_from_json
import keras
from keras import backend as K
import sys


class NumberReco:

    def __init__(self):
        # load json and create model
        json_file = open('src/raspi/numberdetector/numberDetectionPython/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights("src/raspi/numberdetector/numberDetectionPython/model.h5")
        print("Loaded model from disk")

        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    """
    thresPicture: thresPicture
    rect: array: x,y,w,h
    """
    def recoNumber(self, newImage):
        try:
            newImage = cv2.resize(newImage, (28, 28))
            newImage = np.array(newImage)
            newImage = newImage.astype('float32')
            newImage /= 255
            if K.image_data_format() == 'channels_first':
                newImage = newImage.reshape(1, 28, 28)
            #else:
            #    newImage = newImage.reshape(28, 28, 1)
            newImage = np.expand_dims(newImage, axis=0)
            ans = self.model.predict(newImage).argmax()
            print(ans)
        except:
            pass
