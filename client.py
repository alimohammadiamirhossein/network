import socket
import threading
import time
import random

host = '127.0.0.1'
manager_port = 3191
ID = input("enter your ID: ")
port = int(input("enter your port: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()


def connection(rec_data=None, port1=-1):
    while True:
        try:
            client_socket.connect((host, port1))
            print("you connected to your manager")
            client_socket.send(f"{ID}".encode("ascii"))
            receive_data(rec_data)
            break
        except Exception as e:
            time.sleep(1)
            message = e


def receive_data(rec_data=None):
    for _ in range(2):
        message1 = client_socket.recv(1024).decode("ascii")
        # print("data receive", message1)
        rec_data[0] = int(message1)
        if rec_data[0] == ID:
            print(f"client-id {ID} is leader")
            rec_data[1] = True
            rec_data[2] = f"client-id {ID} is leader"
            return


thread = threading.Thread(target=connection, args=(None, manager_port,))
thread.start()
