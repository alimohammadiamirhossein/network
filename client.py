import socket
import threading
import time
import random

host = '127.0.0.1'
manager_port = 3191
ID = input("enter your ID: ")
port = int(input("enter your port: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()


def connection(send_data, port1):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client_socket.connect((host, port1))
            print("you connected to your manager")
            client_socket.send(send_data.encode("ascii"))
            client_socket.close()
            break
        except Exception as e:
            time.sleep(1)
            message = e


def server_receive():
    while True:
        cl1, add1 = server_socket.accept()
        msg = cl1.recv(1024).decode("ascii")
        print(msg)


thread2 = threading.Thread(target=server_receive, args=())
thread2.start()
connection(f"{ID} REQUESTS FOR CONNECTING TO NETWORK ON PORT {port}", manager_port)
