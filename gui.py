from tkinter import *
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget
from utils import Utils


import pyautogui


class Screen():
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("SAP MQTT utility")
        self.window.setGeometry(200,200,560,160)
        self.scr = Tk()
        self.scr.title("SAP MQTT utility")
        self.scr.geometry(str(pyautogui.size()[0]) + "x" + str(pyautogui.size()[1]))
        self.frame = Frame(self.scr)


    def getExcel(self,fileDir):
        print(fileDir)
        rc = Utils.loadData(fileDir)

    def start(self):
        self.frame.grid()
        #height é em termos de rows, width em termos de colunas
        scrWindow = Text(self.frame,width=100,height=1)
        print(scrWindow.size())
        scrWindow.pack()
        btnUpload = Button(master=self.frame,text="Upload Excel",
                           command=lambda: self.getExcel(scrWindow.get(1.0,"end-1c")))
        btnUpload.place(x=25, y=100)
        btnQuit = Button(master=self.frame,text="Quit",command=self.scr.destroy)
        btnQuit.place(x=20, y=150)
        btnUpload.place()
        btnUpload.pack()
        btnQuit.pack()
        self.scr.mainloop()