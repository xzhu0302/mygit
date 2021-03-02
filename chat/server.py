# -*- coding=utf-8
import socket
from threading import Thread
import time
class Server:
    def __init__(self):
        self.server=socket.socket()
        self.server.bind(("127.0.0.1", 8989))
        self.server.listen(5)
        self.clients = []
        self.clients_name_ip={}
        self.get_conn()

    def get_conn(self):
        while True:
            client,address = self.server.accept()
            print(address)
            data = "与服务器连接成功，请先输入昵称"
            client.send(data.encode())
            self.clients.append(client)
            Thread(target=self.get_msg,args=(client,self.clients,self.clients_name_ip,address)).start()
    def get_msg(self,client,clients,clients_name_ip,address):
        name=client.recv(1024).decode()
        clients_name_ip[address]=name
        while True:
            try:
                recv_data=client.recv(1024).decode()
            except Exception as e:
                self.close_client(client,address)
                break
            if recv_data.upper()=="Q":
                self.close_client(client,address)
                break
            for c in clients:
                print(clients_name_ip[address]+" "+time.strftime("%x")+"\n"+recv_data)
                print(type(clients_name_ip[address] + " " + time.strftime("%x") + "\n" + recv_data))

                c.send((clients_name_ip[address]+" "+time.strftime("%x")+recv_data).encode())
    def close_client(self,client,address):
        self.clients.remove(client)
        client.close()
        print(self.clients_name_ip[address]+"已经离开")
        for c in self.clients:
            c.send((self.clients_name_ip[address]+"已经离开").encode())
if __name__=="__main__":
    Server()

