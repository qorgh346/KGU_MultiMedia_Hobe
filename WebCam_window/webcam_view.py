import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from skimage import io
from PyQt5 import QtGui
import numpy as np
import qimage2ndarray
import matplotlib.pyplot as plt

form_image_window = uic.loadUiType("webCam_Window.ui")[0]

class webCamWindow(QDialog,QWidget,form_image_window):

    #Convert video, webcam to grayscale, flip
    def __init__(self):
        super(webCamWindow,self).__init__()
        self.initUI()
        self.show()
        self.width = 200
        self.height = 200

    def initUI(self):
        self.setupUi(self)
        self.home.clicked.connect(self.Home)
        self.connectBtn.clicked.connect(self.connectwebcam)
        self.stopBtn.clicked.connect(self.stop_webcam)
        self.convertBtn.clicked.connect(self.convertVideo)
        self.grayscaleBtn.clicked.connect(self.grayScale)
        self.flipBtn.clicked.connect(self.flipVideo)


    def connectwebcam(self):
        print('connect web cam')
        import cv2
        self.stop_webcam = False
        self.grayscale = False
        self.convert_video = False
        self.flip_90, self.flip_180, self.flip_270 = False, False, False
        self.currentRotation = 0

        cap = cv2.VideoCapture(0)
        while True:
            ret, self.source_image = cap.read()
            init_image = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2RGB)
            self.show_image('input', init_image)

            if self.grayscale:
                image = cv2.cvtColor(init_image, cv2.COLOR_BGR2GRAY)
            elif self.currentRotation == 90:
                image = cv2.rotate(init_image, cv2.ROTATE_90_CLOCKWISE)
            elif self.currentRotation == 180:
                image = cv2.rotate(init_image, cv2.ROTATE_180)
            elif self.currentRotation == 270:
                image = cv2.rotate(init_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                image = init_image
            self.show_image('output', image)

            cv2.waitKey(24)
            if self.stop_webcam:
                break
            if self.convert_video:
                pass



    def show_image(self,label,image):
        qt_image1 = QtGui.QImage(image.data,
                                 self.width,
                                 self.height,
                                 image.strides[0],
                                 QtGui.QImage.Format_RGB888)

        if label == 'input':
            print('input')
            pixmap = QtGui.QPixmap.fromImage(qt_image1)
            self.inputCam.setPixmap(pixmap)
        else:
            print('output!!')
            pixmap = QtGui.QPixmap.fromImage(qt_image1)
            self.outputCam.setPixmap(pixmap)

    def stop_webcam(self):
        self.stop_webcam = True

    def convertVideo(self):
        self.convert_video = True

    def grayScale(self):
        self.currentRotation = 0
        self.grayscale = True

    def flipVideo(self):
        self.grayscale = False
        if self.currentRotation < 360:
            self.currentRotation += 90
            if self.currentRotation == 360:
                self.currentRotation = 0


    def Home(self):
        self.close()
