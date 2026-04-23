import socket

HOST = "192.168.246.29"
PORT = 9002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))

    nome = input("[Cliente] Digite seu nome: ")
    
    cliente.sendall(nome.encode("utf-8"))

    while True :
        mensagem = input("Digite sua mensagem: ")
        cliente.sendall(mensagem.encode("utf-8"))
    