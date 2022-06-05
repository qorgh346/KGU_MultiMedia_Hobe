import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from skimage import io
from PyQt5 import QtGui
import numpy as np
import qimage2ndarray
from matplotlib import pyplot as plt
from PIL import Image

form_image_window = uic.loadUiType("image_click_view.ui")[0]

class histoWindow(QDialog,QWidget,form_image_window):

    def __init__(self,inputImage):
        super(histoWindow,self).__init__()
        self.image = inputImage
        self.initUI()
        self.show()

    def initUI(self):
        print('iniasdsadsadtUI')

        self.setupUi(self)
        self.home.clicked.connect(self.Home)
        self.histogramShowBtn.clicked.connect(self.histoShow)
        self.imgshowBtn.clicked.connect(self.imgShow)
    def histoShow(self):
        print('zzsdfsdffsdfsdfsdf')
        histogram = self.getHistogram()
        histo = np.array(histogram)
        histo = qimage2ndarray.array2qimage(histo)
        qt_histo = QtGui.QPixmap.fromImage(histo)
        self.view_result.setPixmap(qt_histo)

    def imgShow(self):
        img = qimage2ndarray.array2qimage(self.image)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.view_result.setPixmap(qt_img)
    def getHistogram(self):

        plt.hist(self.image.ravel(),bins=256)
        plt.savefig('hist.png')
        hist_img = io.imread('hist.png')
        print('io = > ',hist_img)
        img = Image.open('hist.png')

        img_resize = img.resize((256, 256))

        return img_resize

    def Home(self):
        self.close()
