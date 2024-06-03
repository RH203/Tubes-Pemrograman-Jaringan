import socket
import os

class SingleThreadChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))
        print("Connected to server.")

    def kirim_pesan(self):
        while True:
            message = input("Client: ")
            self.client_socket.send(message.encode('utf-8'))
            if message.lower() == "exit":
                print("Client has closed the connection.")
                self.client_socket.close()
                break

    def terima_pesan(self):
        while True:
            message = self.client_socket.recv(1024).decode('utf-8')
            print("Server: {}".format(message))
            if message.lower() == "exit":
                print("Server has closed the connection.")
                self.client_socket.close()
                break

    def run(self):
        try:
            while True:
                self.kirim_pesan()
                self.terima_pesan()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.client_socket.close()
