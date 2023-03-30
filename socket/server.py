import socket

HOST = "localhost"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("Aguardando conexão do cliente...")
    conn, addr = s.accept()

    with conn:
        print("Conexão estabelecida:", addr)

        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode()
            print("Mensagem recebida do cliente:", message)

            if message == "ping":
                response = "pong"
            elif message == "alo":
                response = "ok"
            else:
                response = "Mensagem inválida"

            conn.sendall(response.encode())
