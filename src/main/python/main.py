from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, qApp, QAction, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QMessageBox, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QStackedWidget, QFormLayout)
import sys
import logging
import json
import os

class MainApp(QWidget):
    def __init__(self, parent=None):
        logging.debug("MainApp:init() instantiated")
        super().__init__()

        self.setFixedSize(350,110)
        quit = QAction("Quit", self)

        self.setWindowTitle("Endian Converter")
        self.formGroupBox = QGroupBox("Enter a sequence of hex digits to convert")
        self.layout = QFormLayout()
        self.hexBytesLineEdit = QLineEdit()
        self.layout.addRow(QLabel("Hex Sequence:"), self.hexBytesLineEdit)
        self.formGroupBox.setLayout(self.layout)

        #Create the bottom layout
        self.bottomLayout = QHBoxLayout()
        self.submitButton = QtWidgets.QPushButton("Convert")
        self.submitButton.clicked.connect(self.convertHexDataActionEvent)
        #self.submitButton.setEnabled(False)
        self.bottomLayout.addWidget(self.submitButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.formGroupBox)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

    def convertHexDataActionEvent(self):
        logging.debug("MainApp:convertHexDataActionEvent() instantiated")
        inputToConvert = self.hexBytesLineEdit.text()
        size = len(inputToConvert)
        if size > 0:
            inputToConvert = inputToConvert.replace(" ", "")
            sizeNoSpaces = len(inputToConvert)
            if (sizeNoSpaces % 2) == 0:
                result = self.convert(inputToConvert)
                logging.debug("Converted hex: " + result)
                qmsg = QtWidgets.QMessageBox(self)
                qmsg.setWindowTitle("Converted Hex")
                qmsg.setText("Use the following values by\r\n(1) double-clicking on the numbers (should turn blue)\r\n (2) right-clicking\r\n (3) select copy\r\n\r\n" + result)
                qmsg.setFixedSize(500,500)
                qmsg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                qmsg.setDefaultButton(QtWidgets.QMessageBox.Ok)
                qmsg.setIcon(QtWidgets.QMessageBox.Information)
                qmsg.setTextInteractionFlags(Qt.TextSelectableByMouse)
                qmsg.exec_()
            else:
                logging.error("Number of hex digits must be even.")    
                QMessageBox.critical(self,
                    "Input Error",
                    "Number of Hex Digits must be even",
                    QMessageBox.Ok)
        else:
            logging.error("Input must be non-empty")
            QMessageBox.critical(self,
                    "Input Error",
                    "Input must be non-empty",
                    QMessageBox.Ok)

        
    def convert(self, hexString):
        logging.debug("MainApp:convert() instantiated")
        answer = ""
        for i in range(len(hexString), 0, -2):
            answer = answer + str(hexString[i-2]) + str(hexString[i-1])
        return answer

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    appctxt = ApplicationContext()
    app = MainApp()
    QApplication.setStyle(QStyleFactory.create('Fusion')) 
    app.show()
    sys.exit(appctxt.app.exec_())