from tkinter import *
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QPushButton, QHBoxLayout, QFormLayout, QMessageBox, \
    QFileDialog, QDialog
from utils import Utils
from PyQt5 import QtCore

import sys
import pyautogui

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self):
        self.appName = "SAP IAM Master Data utility"

    def setupUi(self, Dialog):
        #Dialog.setObjectName(self.appName)
        Dialog.setWindowTitle(self.appName)
        Dialog.resize(800, 600)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(170, 50, 480, 31))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 60, 56, 16))
        self.label.setObjectName("label")
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(669, 50, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.getBrowseCallBack())
        self.textEditStatus = QtWidgets.QTextEdit(Dialog)
        self.textEditStatus.setGeometry(QtCore.QRect(170, 130, 431, 221))
        self.textEditStatus.setObjectName("textEdit_2")
        self.labelStatus = QtWidgets.QLabel(Dialog)
        self.labelStatus.setGeometry(QtCore.QRect(80, 130, 91, 16))
        self.labelStatus.setObjectName("label_2")
        self.btnUpload = QPushButton(Dialog)
        self.btnUpload.setGeometry(QtCore.QRect(580, 530, 93, 28))
        self.btnUpload.setObjectName("pushButton_2")
        self.btnUpload.clicked.connect(lambda: self.getExcel(self.textEdit.toPlainText(),self.textEditStatus))
        self.btnQuit = QPushButton(Dialog)
        self.btnQuit.setGeometry(QtCore.QRect(690, 530, 93, 28))
        self.btnQuit.setObjectName("pushButton_3")
        self.btnQuit.clicked.connect(lambda: sys.exit())

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def getExcel(self,fileDir, textEdit):
        print(fileDir)
        rc = Utils.loadData(fileDir,textEdit)
        if rc == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please enter a valid file!")
            msg.setWindowTitle(self.appName)
            msg.exec()
            #msg.close()
        elif rc == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("File Sucessfully loaded!")
            msg.setWindowTitle(self.appName)
            msg.exec()

    def getBrowseCallBack(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setViewMode(QFileDialog.Detail)
        if fileDialog.exec():
            self.textEdit.setText(fileDialog.selectedFiles()[0])


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        #Dialog.setWindowTitle(_translate("Dialog", "S"))
        self.label.setText(_translate("Dialog", "File:"))
        self.pushButton.setText(_translate("Dialog", "Browse"))
        self.btnUpload.setText(_translate("Dialog", "Upload"))
        self.btnQuit.setText(_translate("Dialog", "Cancel"))
        self.labelStatus.setText("Execution Log:")

class Screen():
    def __init__(self):
        self.app = QApplication([])
        self.appName = "SAP MQTT Measurement utility"
        self.window = Ui_Dialog()

    def getExcel(self,fileDir):
        print(fileDir)
        rc = Utils.loadData(fileDir)
        if rc == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please enter a valid file!")
            msg.setWindowTitle(self.appName)
            msg.exec()
            #msg.close()
        elif rc == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("File Sucessfully loaded!")
            msg.setWindowTitle(self.appName)
            msg.exec()

    def start(self):
        dialog = QDialog()
        self.window.setupUi(dialog)
        dialog.exec()
        #self.window.show()
        #fileForm = QFormLayout()
        #fileDir = QLineEdit()
        #fileForm.addRow("File Directory", fileDir)
        #btnUpload = QPushButton()
        #btnUpload.clicked.connect(lambda: self.getExcel(fileDir.text()))
        #btnUpload.setText("Upload file")
        #btnQuit = QPushButton()
        #btnQuit.setText("Quit")
        #btnQuit.clicked.connect(lambda: sys.exit())
        #btnLayout = QHBoxLayout()
        #btnLayout.addWidget(btnUpload)
        #btnLayout.addWidget(btnQuit)
        #btnLayout.setAlignment(Qt.AlignHCenter)
        #self.window.setLayout(btnLayout)
        #self.window.setLayout(btnLayout)
        #btnLayout.addLayout(fileForm)
        #self.window.setLayout(fileForm)
        #self.window.show()
        #sys.exit(self.app.exec())
        #btnLayout.addWidget(btnUpload,btnQuit)
        #self.frame.grid()
        #height é em termos de rows, width em termos de colunas
        #scrWindow = Text(self.frame,width=100,height=1)
        #scrWindow.pack()
        #btnUpload = Button(master=self.frame,text="Upload Excel",
        #                   command=lambda: self.getExcel(scrWindow.get(1.0,"end-1c")))
        #btnUpload.place(x=25, y=100)
        #btnQuit = Button(master=self.frame,text="Quit",command=self.scr.destroy)
        #btnQuit.place(x=20, y=150)
        #btnUpload.place()
        #btnUpload.pack()
        #btnQuit.pack()
        #self.scr.mainloop()