import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("An error occurred.")
            sock.close()
            break

def main():
    host = '127.0.0.1'  # Using localhost for demonstration
    port = 12345

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("Connected to {}:{}".format(host, port))

        threading.Thread(target=receive_messages, args=(sock,)).start()

        while True:
            message = input()
            sock.send(message.encode('utf-8'))
    except socket.gaierror:
        print("Invalid address.")
    except ConnectionRefusedError:
        print("Connection refused by the server.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
