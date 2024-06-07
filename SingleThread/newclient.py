import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.55.13', 8081))

def receive_message():
    while True:
        try:
            message = client.recv(1024)
            if message:
                print(message.decode('utf-8'))
            else:
                break
        except:
            continue

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

while True:
    message = input()
    client.send(message.encode('utf-8'))