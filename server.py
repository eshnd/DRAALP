import socket
import threading
import json
import os

PORT = 8017
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
MAX_LENGTH_SIZE = 64

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def script(inp):
    print(inp)

def formatting(conn, addr):
    connected = True
    while connected:
        msg_length = (conn.recv(MAX_LENGTH_SIZE).decode('utf-8'))
        if msg_length:
            msg = conn.recv(int(msg_length)).decode('utf-8')
            
            script(msg)
            data = {"MSG": [msg]}
            
            with open(str(addr[0]) + '.json', 'a') as file:
                json.dump(data, file, indent=4)

def start():
    server.listen()
    while(True):
        conn, addr = server.accept()
        thread = threading.Thread(target=formatting, args=(conn, addr))
        thread.start()

print("Server has started")
start()
