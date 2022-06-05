import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from skimage import io
from PyQt5 import QtGui
import numpy as np
import qimage2ndarray

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
        self.flipBtn.clicked.connect(self.filpVideo)

    def connectwebcam(self):
        print('connect web cam')
        import cv2
        self.stop_webcam = False
        self.grayscale = False
        self.convert_video = False
        self.flip = False
        cap = cv2.VideoCapture(0)
        while True:
            ret,self.source_image = cap.read()
            image = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2RGB)
            self.show_image('input', image)
            if self.grayscale:
                image = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2GRAY)
                self.show_image('output', image)

            if self.convert_video:
                pass
            if self.flip:
                pass
            cv2.waitKey(24)
            if self.stop_webcam:
                break
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
        self.grayscale = True

    def filpVideo(self):
        self.filp= True

    def Home(self):
        self.close()
