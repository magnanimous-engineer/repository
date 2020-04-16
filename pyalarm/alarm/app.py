import sys
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QTextEdit, \
    QLabel, QComboBox, QCheckBox, QFileDialog
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor
import alarm
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QThread, QObject

#####
class Thread(threading.Thread):
    def __init__(self, identity, name):
        self.identity = identity
        self.name = name

    def run(self):
        alarm.runCheck()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Alarm'
        self.top = 10
        self.left = 10
        self.width = 500
        self.height = 600
        self.initUI()

    def initUI(self):

        dark = QColor(25, 25, 50)
        white = QColor(255, 255, 255)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), white)

        widgets = QWidget()
        ########################## I like my comments green! ########################
        self.select = QComboBox(self)
        self.select.move(325, 50)
        self.select.resize(125, 25)
        self.select.addItem("0:30:0")
        self.select.addItem("1:0:0")
        self.select.currentIndexChanged.connect(self.selectChange)

        self.newtimer = QPushButton(self)
        self.newtimer.move(5, 80)
        self.newtimer.setText("Add Timer")
        self.newtimer.clicked.connect(self.timer)

        self.starttimer = QPushButton(self)
        self.starttimer.move(325, 80)
        self.starttimer.setText("Start Timer")

        self.secondL = QLabel(self)
        self.secondL.move(190, 27)
        self.secondL.setText("Seconds:")

        self.minuteL = QLabel(self)
        self.minuteL.move(107, 27)
        self.minuteL.setText("Minutes:")

        self.hourl = QLabel(self)
        self.hourl.move(25, 27)
        self.hourl.setText("Hours:")

        self.hourIn = QLineEdit(self)
        self.hourIn.move(5, 50)
        self.hourIn.resize(80, 25)
        # self.hourIn.setStyleSheet("QLineEdit { background-color: rgb(25, 25, 50); color: rgb(255, 255, 255)}")

        self.minuteIn = QLineEdit(self)
        self.minuteIn.move(90, 50)
        self.minuteIn.resize(80, 25)

        self.secondIn = QLineEdit(self)
        self.secondIn.move(175, 50)
        self.secondIn.resize(80, 25)
        ######################################################################
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setPalette(p)
        ######################################################################
        self.show()
        widgets.show()

    def selectChange(self):
        print(self.select.itemText(self.select.currentIndex()))

    def timer(self):
        h = self.hourIn.text()
        m = self.minuteIn.text()
        s = self.secondIn.text()
        if h.replace(" ", "") == "":
            h = 00
        if m.replace(" ", "") == "":
            m = 00
        if s.replace(" ", "") == "":
            s = 00
        try:
            t = (int(h) * 3600) + (int(m) * 60) + int(s)
            if t == 0:
                QMessageBox.about(self, "Please fill out time", "The timer must be at least one second long.")
                t = None
        except:
            self.hourIn.clear()
            self.minuteIn.clear()
            self.secondIn.clear()
            QMessageBox.about(self, "Wrong number type!",
                              "Please type in an integer, no decimals or text! Numbers too big can also raise an error.")
        try:
            if t is not None:
                alarm.timer(t)
                self.select.addItem(str(h) + ":" + str(m) + ":" + str(s))
        except:
            pass
        self.hourIn.clear()
        self.minuteIn.clear()
        self.secondIn.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
