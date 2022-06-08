import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from skimage import io
from PyQt5 import QtGui
import numpy as np
import qimage2ndarray
import cv2

form_image_window = uic.loadUiType("filterWindow.ui")[0]

class filterWindow(QDialog,QWidget,form_image_window):

    def __init__(self,input_image):
        super(filterWindow,self).__init__()
        self.image = input_image
        self.initUI()
        self.show()


    def initUI(self):

        self.setupUi(self)
        self.home.clicked.connect(self.Home)
        self.hsKValue.valueChanged.connect(self.change_kValue)
        self.blurBtn.clicked.connect(self.blurShow)
        self.sharpBtn.clicked.connect(self.sharpShow)
        # self.uploadBtn.clicked.connect(self.image_input)


    def blurShow(self):

        blur_flag = int(self.hsKValue.value() / 10)
        self.setKvalue.setText(str(blur_flag))
        blur_img = cv2.GaussianBlur(self.image, (45, 45), blur_flag)
        # temp_img = cv2.rotate(blur3, cv2.ROTATE_180)

        # result = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)

        img = np.array(blur_img)
        img = qimage2ndarray.array2qimage(img)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)

    def sharpShow(self):

        sharpen_flag = int(self.hsKValue.value() / 10) + 5
        self.setKvalue.setText(str(sharpen_flag))
        kernel_sharpening = np.array([[-1,-1,-1],
                                      [-1,sharpen_flag,-1],
                                      [-1,-1,-1]])
        sharpened = cv2.filter2D(self.image,-1,kernel_sharpening)
        img = qimage2ndarray.array2qimage(sharpened)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)


    def change_kValue(self):
        k = self.hsKValue.value() / 100
        image_k = self.image * k
        self.setKvalue.setText(str(k))

        img = qimage2ndarray.array2qimage(image_k)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)

    def Home(self):
        self.close()
