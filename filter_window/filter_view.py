import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from skimage import io
from PyQt5 import QtGui
import numpy as np
import qimage2ndarray

form_image_window = uic.loadUiType("filterWindow.ui")[0]

class filterWindow(QDialog,QWidget,form_image_window):

    def __init__(self):
        super(filterWindow,self).__init__()
        self.initUI()
        self.show()

    def initUI(self):

        self.setupUi(self)
        self.home.clicked.connect(self.Home)
        # self.uploadBtn.clicked.connect(self.image_input)


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
