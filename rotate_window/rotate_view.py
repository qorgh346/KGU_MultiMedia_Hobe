import math
import cv2
import numpy as np
import scipy
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
import qimage2ndarray
from scipy import ndimage

form_image_window = uic.loadUiType("rotateWindow.ui")[0]


class rotateWindow(QDialog, QWidget, form_image_window):

    def __init__(self, inputImage):
        super(rotateWindow, self).__init__()
        self.image = inputImage
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.home.clicked.connect(self.Home)
        self.imgshowBtn.clicked.connect(self.img_show)
        self.rotateBtn.clicked.connect(self.img_rotate)
        self.scalingBtn.clicked.connect(self.img_scaling)
        self.flipLRBtn.clicked.connect(self.img_flip_LR)
        self.flipTBBtn.clicked.connect(self.img_flip_TB)
        self.warpColBtn.clicked.connect(self.img_warp_Col)
        self.cropBtn.clicked.connect(self.img_crop)
        '''self.warpColBtn.clicked.connect(self.img_warp_Col)
        self.warpRowBtn.clicked.connect(self.img_warp_Row)
        self.cropBtn.clicked.connect(self.img_crop)'''

        self.currentRotation = 0

    def img_show(self):
        img = qimage2ndarray.array2qimage(self.image)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)

    def img_rotate(self):
        if self.currentRotation < 360:
            self.currentRotation += 90
            if self.currentRotation == 360:
                self.currentRotation = 0

        if self.currentRotation == 90:
            im_rotate = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        elif self.currentRotation == 180:
            im_rotate = cv2.rotate(self.image, cv2.ROTATE_180)
        elif self.currentRotation == 270:
            im_rotate = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            im_rotate = self.image

        img = qimage2ndarray.array2qimage(im_rotate)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)

    def img_scaling(self):
        im_scaling = cv2.resize(self.image, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        img = qimage2ndarray.array2qimage(im_scaling)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)
    def img_crop(self):
        x = 50
        y = 50
        h = 250
        w = 250
        img = self.image[y: y + h, x: x + w,:]
        img = qimage2ndarray.array2qimage(img)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)

    def img_flip_LR(self):
        im_f_lr = cv2.flip(self.image, 1)  # 좌우반전 1
        img = qimage2ndarray.array2qimage(im_f_lr)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)

    def img_flip_TB(self):
        im_f_tb = cv2.flip(self.image, 0)  # 상하반전 0
        img = qimage2ndarray.array2qimage(im_f_tb)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)

    def img_warp_Col(self):
        print(self.image.shape)
        print(type(self.image))
        rows = self.image.shape[0]
        cols = self.image.shape[1]

        img_output = np.zeros(self.image.shape, dtype=self.image.dtype)

        for i in range(rows):
            for j in range(cols):
                offset_x = int(20.0 * math.sin(2 * 3.14 * i / 150))
                offset_y = int(20.0 * math.cos(2 * 3.14 * j / 150))
                if i + offset_y < rows and j + offset_x < cols:
                    img_output[i, j] = self.image[(i + offset_y) % rows, (j + offset_x) % cols]
                else:
                    img_output[i, j] = 0
        img = qimage2ndarray.array2qimage(img_output)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)
        # cv2.imshow('Multidirectional wave', img_output)

    '''def img_warp_Col(self):
        img = qimage2ndarray.array2qimage(self.image)
        rows, cols = img.shape[0], img.shape[1]
        img_output = np.zeros((rows, cols))

        for i in range(rows):
            for j in range(cols):
                offset_x = int(40.0 * math.sin(2*3.14*i / 180))
                if j + offset_x < rows:
                    img_output[i, j] = img[i, (j + offset_x) % cols]'''

    # def image_input(self):
    #     print('image')
    #     img = QFileDialog.getOpenFileNames(self, 'image')
    #     img_path = self.image_view(img[0][0])
    #     self.image_view(img_path)
    #
    # def image_view(self,file_name):
    #
    #     try:
    #         print(file_name)
    #         img = io.imread(file_name)
    #         img = qimage2ndarray.array2qimage(img)
    #         gui_image = QtGui.QPixmap.fromImage(img)
    #
    #         self.input_view.setPixmap(gui_image)
    #     except:
    #         print('error')

    def Home(self):
        self.close()