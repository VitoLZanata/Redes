import socket
import threading
import random
import time

HOST = "192.168.246.29"
PORT = 9002
U = "utf-8"
N_J = 2  #Numero de Jogadores
N_R = 3  # Numero de Rodadas
ALFABETO = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

NOME = [None] * N_J
CEP = [None] * N_J
MEU_PROFESSOR = [None] * N_J
COR = [None] * N_J
PONTOS = [0] * N_J 

CONEXOES = []
NOMES = [None] * N_J
LETRA_COMPARTILHADA = [None]

barreira = threading.Barrier(N_J)

def verificar_ocorrencia_pontos(lista, j):
    #x = 1 se for repetido ou vazio, x = 3 se for único
    if not lista[j] or lista[j] == "":
        x = 0
    elif lista.count(lista[j]) > 1:
        x = 1
    else:
        x = 3
    
    PONTOS[j] += x
    return x

def jogo(conn, addr, jogador_id):
    print(f"[Server] Jogador {jogador_id} conectado: {addr}")
    conn.sendall(f"\n[Server] Você é o jogador {jogador_id + 1}.".encode(U))
    
    nome_recebido = conn.recv(1024).decode(U).strip()
    NOMES[jogador_id] = nome_recebido
    
    j = 0
    while j < N_R:
        # jogador 0 sorteia a letra para todos
        if jogador_id == 0:
            letra_sorteada = random.choice(ALFABETO)
            LETRA_COMPARTILHADA[0] = letra_sorteada
        
        barreira.wait() #aguarda sorteio da letra

        letra = LETRA_COMPARTILHADA[0]
        conn.sendall(f"\n--- RODADA {j+1} --- \nLetra da rodada: {letra}\n".encode(U))
        
        #.strip() remove espaços extras e o \n do terminal
        NOME[jogador_id] = conn.recv(1024).decode(U).strip().upper()
        CEP[jogador_id] = conn.recv(1024).decode(U).strip().upper()
        MEU_PROFESSOR[jogador_id] = conn.recv(1024).decode(U).strip().upper()
        COR[jogador_id] = conn.recv(1024).decode(U).strip().upper()
        
        #espera todos os jogadores enviarem as respostas
        barreira.wait()
        
        # Calcula pontos chamando seu método para cada lista
        v1 = verificar_ocorrencia_pontos(NOME, jogador_id)
        v2 = verificar_ocorrencia_pontos(CEP, jogador_id)
        v3 = verificar_ocorrencia_pontos(MEU_PROFESSOR, jogador_id)
        v4 = verificar_ocorrencia_pontos(COR, jogador_id)
        
        total_da_rodada = v1 + v2 + v3 + v4
        
        #espera todos calcularem antes de enviar o status
        barreira.wait()
        
        msg_status = f"Voce fez {total_da_rodada} pontos nesta rodada. Total acumulado: {PONTOS[jogador_id]}\n"
        conn.sendall(msg_status.encode(U))
        
        barreira.wait()
        j += 1

    #final do Jogo
    barreira.wait() # Garante que todos saíram do loop de rodadas
    
    #Vencedor
    maior_pontuacao = max(PONTOS)
    vencedor_id = PONTOS.index(maior_pontuacao)
    
    anuncio = f"\nFIM DE JOGO!\nO VENCEDOR FOI O JOGADOR {NOMES[vencedor_id]} COM {maior_pontuacao} PONTOS!\n"
    conn.sendall(anuncio.encode(U))
    
    print(f"[Server] Conexão com Jogador {jogador_id + 1} encerrada.")
    conn.close()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        
        print(f"Servidor STOP rodando em {HOST}:{PORT}")
        print(f"Aguardando {N_J} jogadores...")
        
        idx = 0
        while idx < N_J:
            conn, addr = server.accept()
            CONEXOES.append(conn)
            
            thread = threading.Thread(
                target=jogo, 
                args=(conn, addr, idx)
            )
            thread.start()
            idx += 1
            
        print("[Server] Todos os jogadores conectaram. Partida iniciada!")

if __name__ == "__main__":
    iniciar_servidor()