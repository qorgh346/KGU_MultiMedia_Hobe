import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from skimage import io
from PyQt5 import QtGui
import numpy as np
import qimage2ndarray
import cv2
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)

form_image_window = uic.loadUiType("./yolo_Window.ui")[0]


class yoloWindow(QDialog, QWidget, form_image_window):

    def __init__(self):
        super(yoloWindow, self).__init__()
        self.initUI()
        self.show()
        self.start = True
        self.yolo_network = yoloNetwork(weight_path='yolo_window/yolov3.weights',cfg_path='yolo_window/yolov3.cfg',classlist_path='yolo_window/coco.names')
    def initUI(self):

        self.setupUi(self)
        self.home.clicked.connect(self.Home)
        self.stop.clicked.connect(self.stopVideo)
        self.play.clicked.connect(self.playVideo)
        self.openbtn.clicked.connect(self.abrir)


        # self.uploadBtn.clicked.connect(self.image_input)
    def playVideo(self):
        self.start = True
        self.yolo_process(self.cap)
    def stopVideo(self):
        self.start = False
    def Home(self):
        self.close()

    def show_image(self,label,image):

        if label == 'input':
            qt_image1 = QtGui.QImage(image.data,
                                     400,
                                     400,
                                     image.strides[0],
                                     QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qt_image1)
            self.inputVideo.setPixmap(pixmap)
            print('ok input')
        else:
            yoloImage,label = self.yolo_network.process(image)
            print('label == ',label)
            print('label : : :: ',yoloImage.data)
            qt_image1 = QtGui.QImage(yoloImage.data,
                                     400,
                                     400,
                                     yoloImage.strides[0],
                                     QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qt_image1)
            self.outputVideo.setPixmap(pixmap)
            self.counting.setText('Counting : {}'.format(label))
    #                 self.frameLabel.setText("No camera connected.")
    def yolo_process(self,cap):

        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 영상의 넓이(가로) 프레임
        frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 영상의 높이(세로) 프레임

        frame_size = (frameWidth, frameHeight)
        print('frame_size={}'.format(frame_size))

        frameRate = 16

        while True:

            retval, frame = cap.read()
            frame = cv2.resize(frame, dsize=(416, 416), interpolation=cv2.INTER_AREA)
            print(frame.shape)
            # 한 장의 이미지(frame)를 가져오기
            # 영상 : 이미지(프레임)의 연속
            # 정상적으로 읽어왔는지 -> retval
            # 읽어온 프레임 -> frame
            if self.start:
                if not (retval):  # 프레임정보를 정상적으로 읽지 못하면
                    break  # while문을 빠져나가기
                self.show_image('input', frame)
                self.show_image('output', frame)
                key = cv2.waitKey(frameRate)
                if key == 27:
                    break

            else:
                break
        cv2.destroyAllWindows()
    def abrir(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona los mediose",
                                                  ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")

        self.fileName = fileName
        self.cap = cv2.VideoCapture(fileName)
        self.yolo_process(self.cap)

class yoloNetwork:
    #self.yolo_network = yoloNetwork(weight_path='./yolov3.weights',cfg_path='./yolov3.cfg',classlist_path='./coco.names')

    def __init__(self,weight_path,cfg_path,classlist_path):
        self.net = cv2.dnn.readNet(weight_path, cfg_path)
        # self.classes = []
        with open(classlist_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
    def process(self,image):
        # Detecting objects
        orgin_image = cv2.resize(image, dsize=(416, 416), interpolation=cv2.INTER_AREA)
        blob = cv2.dnn.blobFromImage(orgin_image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        image,result = self.visual_window(outs,blob,orgin_image,mode='video')
        return image,result

    def visual_window(self,outs,image,orgin_image,mode='visual'):

        channels,height,width  = image.shape[1:]

        class_ids = []
        confidences = []
        boxes = []
        car_cout = 0
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # 좌표
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        #noise remove
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                color = self.colors[i]
                if label == 'car':
                    car_cout += 1
                cv2.rectangle(orgin_image, (x, y), (x + w, y + h), color, 2)
                cv2.putText(orgin_image, label, (x, y + 30), font, 1, color, 1)

        if mode =='visual':
            a = cv2.imwrite("Image.png", orgin_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        return orgin_image,car_cout


if __name__ == '__main__':
    yolo_network = yoloNetwork(weight_path='./yolov3.weights', cfg_path='./yolov3.cfg', classlist_path='./coco.names')
    img = cv2.imread('../../images/car.png')
    a = yolo_network.process(img)
