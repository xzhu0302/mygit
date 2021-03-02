from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import sys
import socket
from threading import Thread
class Client(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(600,300,360,300)
        self.setWindowTitle("聊天室")
        palette=QtGui.QPalette()
        bg=QtGui.QPixmap(r"./image/background.png")
        palette.setBrush(self.backgroundRole(),QtGui.QBrush(bg))
        self.setPalette(palette)
        self.add_ui()
        self.client=socket.socket()
        self.client.connect(("127.0.0.1",8989))
        self.work_thread()
    def add_ui(self):
        self.content=QTextBrowser(self)
        self.content.setGeometry(30,30,300,150)
        self.message=QLineEdit(self)
        self.message.setPlaceholderText(u"输入发送内容")
        self.message.setGeometry(30,200,300,30)
        self.button=QPushButton("发送",self)
        self.button.setFont(QFont("微软雅黑",10,QFont.Bold))
        self.button.setGeometry(270,250,60,30)

    def send_msg(self):
        msg=self.message.text()
        self.client.send(msg.encode())
        if msg.upper()=="Q":
            self.client.close()
            self.destroy()
        self.message.clear()
    def recv_msg(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                print(data)
                data=data+"\n"
                self.content.append(data)
            except:
                exit()
    def btn_send(self):
        self.button.clicked.connect(self.send_msg)
    def work_thread(self):
        Thread(target=self.btn_send).start()
        Thread(target=self.recv_msg).start()
if __name__=="__main__":
    app=QApplication(sys.argv)
    client=Client()
    client.show()
    sys.exit(app.exec_())

