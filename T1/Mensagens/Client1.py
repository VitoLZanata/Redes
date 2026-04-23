# Cliente
import socket

HOST = "192.168.246.29"
PORT = 9003

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        m = s.recv(1024).decode("utf-8")
        print(m)
