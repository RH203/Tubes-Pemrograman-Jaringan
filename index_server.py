from multithread.server import ChatServer
from SingelThread.server import SingelChatClient
import os

if __name__ == "__main__":
    os.system("cls")
    print("Welcome to Chat Server!")

    threading_choice = input("Do you want to use multithreading? (yes/no): ").lower().strip()
    if threading_choice == 'yes':
        server = ChatServer()
        server.receive()
    else:
        server = SingelChatClient()
        server.message_receive()
