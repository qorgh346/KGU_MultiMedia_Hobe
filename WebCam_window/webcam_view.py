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
        self.openVideoBtn.clicked.connect(self.openVideo)
        self.grayscaleBtn.clicked.connect(self.grayScale)
        self.flipBtn.clicked.connect(self.flipVideo)

    # webcam 열어서 grayscale과 flip 적용하는 부분
    def connectwebcam(self):
        print('connect web cam')
        import cv2
        self.stop_webcam = False
        self.grayscale = False
        self.open_video = False
        #self.flip_90, self.flip_180, self.flip_270 = False, False, False
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
            if self.open_video:
                pass

    # video 파일 열어서 grayscale과 flip 적용하는 부분
    def openVideo(self):
        from PyQt5 import QtWidgets, QtCore

        print('connect video')
        import cv2
        self.stop_webcam = False
        self.grayscale = False
        self.open_video = False
        # self.flip_90, self.flip_180, self.flip_270 = False, False, False
        self.currentRotation = 0

        # 동영상 파일 열기
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                'Open File',
                                                                QtCore.QDir.rootPath(),
                                                                '*.*')
        cap = cv2.VideoCapture(fileName)

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
            if self.open_video:
                pass

    # video 보여주는 부분
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

    # video stop 하는 부분
    def stop_webcam(self):
        self.stop_webcam = True

    # grayscale 적용하기 위한 함수
    def grayScale(self):
        self.currentRotation = 0
        self.grayscale = True

    # flip 적용하기 위한 함수
    def flipVideo(self):
        self.grayscale = False
        if self.currentRotation < 360:
            self.currentRotation += 90
            if self.currentRotation == 360:
                self.currentRotation = 0

    # 현재 화면 끄는 함수
    def Home(self):
        self.close()
