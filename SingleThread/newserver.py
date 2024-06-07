import socket
import select
import sys
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('192.168.55.13', 8081))
server.listen(100)

clients = []

def broadcast(message, connection):
    for client in clients:
        if client != connection:
            client.send(message)

def client_thread(connection, address):
    connection.send("Selamat datang di chat room!")
    while True:
        try:
            message = connection.recv(1024)
            if message:
                broadcast(message, connection)
            else:
                remove(connection)
                connection.close()
                break
        except:
            continue

while True:
    connection, address = server.accept()
    clients.append(connection)
    start_new_thread(client_thread, (connection, address))