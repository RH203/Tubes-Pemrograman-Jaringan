import socket

class SingleThreadChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        print("Server is waiting for a connection...")

    def kirim_pesan(self, client_socket):
        while True:
            message = input("Server: ")
            client_socket.send(message.encode('utf-8'))
            if message.lower() == "exit":
                print("Server has closed the connection.")
                client_socket.close()
                break

    def terima_pesan(self, client_socket):
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            print("Client: {}".format(message))
            if message.lower() == "exit":
                print("Client has closed the connection.")
                client_socket.close()
                break

    def run(self):
        client_socket, client_addr = self.server_socket.accept()
        print("Client connected from: {}".format(client_addr))
        try:
            while True:
                self.terima_pesan(client_socket)
                self.kirim_pesan(client_socket)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            client_socket.close()
            self.server_socket.close()
