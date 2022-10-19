"""
This code was developed using TechWithTim's tutorial on sockets.
It's not original code but it is hand typed (no it's not)
"""


from http import client
import socket 
import threading

HEADER = 16
PORT = 6969
SERVER = '127.0.0.1'  # socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            else:   # Belt message to all other clients
                print(f'[DEBUG]: Client Addr: {[c[1] for a, c in clients]}')
                for client_socket, client_addr in clients:
                    if client_addr != addr:
                        # Fix weird bug: client addr has all client addresses
                        msg = f'{str(client_addr[1])}: {msg}'
                        print(f'[Message]: {msg}')
                        send_to_client(msg, client_socket)
                    
                print(f'[Message] Sent to all clients')    
                    
            print(f"[{addr}] {msg}")

    conn.close()
    clients.remove((conn, addr))

def send_to_client(msg, client_socket):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length = send_length + b' ' * (HEADER - len(send_length))
    try:
        client_socket.send(send_length)
        client_socket.send(message)  
    except:
        print(f'[DEBUG]: {send_length=}, {msg=}')

def start():
    server.listen()
    print(f"[LISTENING]: Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        clients.append((conn, addr))
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")


print("[STARTING]: server is starting...")
start()