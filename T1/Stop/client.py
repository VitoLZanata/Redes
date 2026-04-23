import socket


HOST = "192.168.246.29"
PORT = 9002
U = "utf-8"
N_R = 3 

def pedir_entrada_valida(categoria, letra_alvo):
    while True:
        valor = input(f"{categoria}: ").strip().upper()
        if valor and valor[0].upper() == letra_alvo.upper():
            return valor
        print(f"Entrada inválida! Deve começar com {letra_alvo}.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    print(f"[*] Conectado ao servidor {HOST}:{PORT}")
    print(cliente.recv(1024).decode(U).strip())
    nome = input("Digite seu nome: ")
    cliente.sendall(nome.encode(U))

    j = 0
    while j < N_R:
        # 1. Recebe a letra da rodada
        mensagem_servidor = cliente.recv(1024).decode(U).strip()
        print(mensagem_servidor)
        letra_obrigatoria = mensagem_servidor[-1].upper()
        print(f"\n--- RODADA INICIADA! Todas as palavras devem começar com: {letra_obrigatoria} ---")
        nome_validado = pedir_entrada_valida("NOME", letra_obrigatoria)
        cliente.sendall(nome_validado.encode(U))

        cep_validado = pedir_entrada_valida("CEP", letra_obrigatoria)
        cliente.sendall(cep_validado.encode(U))

        prof_validado = pedir_entrada_valida("MEU PROFESSOR DE REDES É", letra_obrigatoria)
        cliente.sendall(prof_validado.encode(U))

        cor_validada = pedir_entrada_valida("COR", letra_obrigatoria)
        cliente.sendall(cor_validada.encode(U))
        print("\n[*] Aguardando processamento da rodada...")

        # 3. Recebe a parcial de pontos
        status_pontos = cliente.recv(1024).decode(U)
        print(status_pontos)

        j += 1

    # 4. Recebe o anúncio final do vencedor
    anuncio_final = cliente.recv(1024).decode(U)
    print(anuncio_final)

