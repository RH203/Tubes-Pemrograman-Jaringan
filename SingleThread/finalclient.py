import socket
import os

class SingleChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.nickname = input("Enter your nickname: ")

    def start_chatting(self):
        self.receive_write_loop()

    def receive_write_loop(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    print(message)

                message = input("")
                message_lower = message.lower()

                if message_lower in ['audio', 'image', 'video']:
                    file_path = input("Enter the path of the file: ")
                    if os.path.isfile(file_path):
                        file_type = message_lower
                        self.send_file(file_path, file_type)
                    else:
                        print("File not found.")
                else:
                    message = f'{self.nickname}: {message}'
                    self.client.send(message.encode('ascii'))
            except Exception as e:
                print(f"An error occurred! Unable to send/receive message. Error: {e}")
                self.client.close()
                break

    def send_file(self, file_path, file_type):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                file_name = os.path.basename(file_path)
                header = f'{self.nickname}: {file_type} {file_name} {len(file_data)}'.encode('ascii')
                self.client.send(header + b'\n' + file_data)
                print(f"Sent {file_type} file: {file_name}")
        except Exception as e:
            print(f"An error occurred while sending the file. Error: {e}")

client = SingleChatClient()
client.start_chatting()
