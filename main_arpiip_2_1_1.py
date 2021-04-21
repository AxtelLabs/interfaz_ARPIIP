
from arpiip_2_1_1 import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

import cv2
import sys

from PyQt5.QtCore import QTimer

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, 491, 301, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(491, 301, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow, Thread):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        # Change to second screen
        self.pushmebutton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.addCam.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.closePop.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        # Change to third screen
        self.addCamsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.camButton.clicked.connect(self.controlTimer)



    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, 491, 301, step, QImage.Format_RGB888)
        # show image in img_label
        self.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(2)
            # update control_bt text
            self.camButton.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.camButton.setText("Start")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())