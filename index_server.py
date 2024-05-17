from multithread.server import ChatServer
import os

if __name__ == "__main__":
    os.system("cls")
    print("Welcome to Chat Server!")

    threading_choice = input("Do you want to use multithreading? (yes/no): ").lower().strip()
    if threading_choice == 'yes':
        server = ChatServer()
        server.receive()
    else:
        print("Single threading is not implemented yet.")
