import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 9002

PORT_CLIENT1 = 9003

conexoes = []
fila = []

semaforo = threading.Semaphore(1)
semaforoFila = threading.Semaphore(1)

def receber_mensagem_fila(conn, addr):
    print(f"[Server] Nova conexão {addr[0]}", flush=True)
    
    nome = conn.recv(1024).decode("utf-8")
    
    while True:
        mensagem = conn.recv(1024).decode("utf-8")
        
        hora = datetime.now().strftime("%H:%M:%S")  
        result = f"[{nome} ({addr[0]}) {hora}]\n{mensagem}"
        
        with semaforoFila:
            fila.append(result)
        
 
def enviar_mensagens_da_fila():
    while True:
        semaforoFila.acquire()
            
        mensagens_para_enviar = list(fila)
        fila.clear()
        
        semaforoFila.release()

        for msg in mensagens_para_enviar:
            msg_bytes = msg.encode("utf-8") 
            
            for conn in conexoes:
                conn.sendall(msg_bytes)

def thread_conexoes():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT} para usuários")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(
                target=receber_mensagem_fila,
                args=(conn, addr),
                daemon=True
            )
            thread.start()

def thread_enviar():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server2:
        server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server2.bind((HOST, PORT_CLIENT1))
        server2.listen()

        threadResposta = threading.Thread(target=enviar_mensagens_da_fila)
        threadResposta.start()

        while True:
            connR, a = server2.accept()
            conexoes.append(connR)
        

def iniciar_servidor():
    
    thread_conn = threading.Thread(
        target=thread_conexoes,
        args=(),    
    )
    thread_conn.start()

    thread_envio = threading.Thread(
        target=thread_enviar,
        args=()
    )
    thread_envio.start()    
    
if __name__ == "__main__":
    iniciar_servidor()