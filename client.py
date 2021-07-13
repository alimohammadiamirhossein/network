import socket
import threading
import time
import random
host = '127.0.0.1'
manager_port = 31950
ID = input("enter your ID: ")
port = int(input("enter your port: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
