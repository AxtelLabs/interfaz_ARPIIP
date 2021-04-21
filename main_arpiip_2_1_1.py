
from arpiip_2_1_0 import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets

class Dialog(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)

        self.pushmebutton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        self.addCamsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        self.addCam.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        self.closePop.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())