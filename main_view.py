import PyQt5.QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import qimage2ndarray
from skimage import io
from PyQt5 import QtGui
import numpy as np
from PyQt5.QtWidgets import *
from PIL import Image
from skimage.transform import resize
import cv2

class MultiMedia_Main_app(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(MultiMedia_Main_app,self).__init__()

        loadUi('multimedia_project_main.ui',self)

        self.histogramPart.clicked.connect(self.go_histogramPart)
        self.filterPart.clicked.connect(self.go_filterPart)
        self.saveImgePart.clicked.connect(self.go_saveImgePart)
        self.rotatePart.clicked.connect(self.go_rotatePart)
        self.uploadBtn.clicked.connect(self.image_input)
        self.webCamBtn.clicked.connect(self.webcamStart)
        self.yolov5Btn.clicked.connect(self.go_yolov5)

    def go_yolov5(self):

        from yolo_window.yolo_view import yoloWindow
        import sys

        self.hide()
        self.player = yoloWindow()
        self.player.exec()  # 두번째 창 닫을때 까지 기다림
        self.show()  # 두번째창 닫으면 다시 메인 창 보여짐


    def webcamStart(self):
        from WebCam_window.webcam_view import webCamWindow

        self.hide()
        self.webcam_window = webCamWindow()  #
        self.webcam_window.exec()  # 두번째 창 닫을때 까지 기다림
        self.show()  # 두번째창 닫으면 다시 메인 창 보여짐

    def image_input(self):
        img = QFileDialog.getOpenFileNames(self, 'image')
        self.image_view(img[0][0])
        # self.image_view(img_path)

    def image_view(self,file_name):

        try:
            img = io.imread(file_name)
            self.input_image = cv2.resize(img, dsize=(300, 300), interpolation=cv2.INTER_CUBIC)            # img_resize = resize(self.input_image,(300,300))
            img = qimage2ndarray.array2qimage(self.input_image)

            gui_image = QtGui.QPixmap.fromImage(img)

            self.input_view.setPixmap(gui_image)
        except:
            print('')

    def go_histogramPart(self):
        from histogram_window.histo_view_main import histoWindow

        self.hide()
        self.histo_window = histoWindow(self.input_image)  #
        self.histo_window.exec()  # 두번째 창 닫을때 까지 기다림
        result_image = self.histo_window.getHistogram()
        img = np.array(result_image)
        img = qimage2ndarray.array2qimage(img)
        qt_img = QtGui.QPixmap.fromImage(img)
        self.result_view.setPixmap(qt_img)
        self.show()  # 두번째창 닫으면 다시 메인 창 보여짐

    def go_filterPart(self):

        from filter_window.filter_view import filterWindow

        self.hide()
        self.filter_window = filterWindow(self.input_image)  #
        self.filter_window.exec()  # 두번째 창 닫을때 까지 기다림
        self.show()  # 두번째창 닫으면 다시 메인 창 보여짐
    def go_rotatePart(self):
        from rotate_window.rotate_view import rotateWindow
        # print('start')
        self.hide()
        self.rotate_window = rotateWindow(self.input_image)  #
        self.rotate_window.exec()  # 두번째 창 닫을때 까지 기다림
        self.show()  # 두번째창 닫으면 다시 메인 창 보여짐
    def go_saveImgePart(self):
        #업로드 된 이미지를 jpg,png, 등 확장자로 변환 후 저장코드 작성
        # print(self.input_image)
        import cv2
        cv2.imwrite("target.jpg", self.input_image)

def main():
    import sys
    app = PyQt5.QtWidgets.QApplication([])
    window = MultiMedia_Main_app()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()