from tkinter import *
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QPushButton, QHBoxLayout, QFormLayout, QMessageBox
from utils import Utils
from PyQt5.QtCore import Qt

import sys


import pyautogui


class Screen():
    def __init__(self):
        self.app = QApplication([])
        self.appName = "SAP MQTT utility"
        self.window = QWidget()
        self.window.setWindowTitle(self.appName)
        self.window.setGeometry(0,0,pyautogui.size()[0],pyautogui.size()[1])
        #self.scr = Tk()
        #self.scr.title("SAP MQTT utility")
        #self.scr.geometry(str(pyautogui.size()[0]) + "x" + str(pyautogui.size()[1]))
        #self.frame = Frame(self.scr)


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
        self.window.show()
        fileForm = QFormLayout()
        fileDir = QLineEdit()
        fileForm.addRow("File Directory", fileDir)
        btnUpload = QPushButton()
        btnUpload.clicked.connect(lambda: self.getExcel(fileDir.text()))
        btnUpload.setText("Upload file")
        btnQuit = QPushButton()
        btnQuit.setText("Quit")
        btnQuit.clicked.connect(lambda: sys.exit())
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btnUpload)
        btnLayout.addWidget(btnQuit)
        #btnLayout.setAlignment(Qt.AlignHCenter)
        #self.window.setLayout(QVBoxLayout())
        self.window.setLayout(btnLayout)
        btnLayout.addLayout(fileForm)
        self.window.show()
        sys.exit(self.app.exec())
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