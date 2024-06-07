import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("An error occurred.")
            client_socket.close()
            break

def main():
    host = '0.0.0.0'  # Listen on all interfaces
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Waiting for a connection...")
    client_socket, addr = server_socket.accept()
    print("Connected to {}:{}".format(addr[0], addr[1]))

    threading.Thread(target=handle_client, args=(client_socket,)).start()

    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
