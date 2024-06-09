import socket
import threading
import os


class ChatServer:
  def __init__(self, host='0.0.0.0', port=5555):
    self.host = host
    self.port = port
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((host, port))
    self.server.listen()
    self.clients = []
    self.nicknames = []

  def broadcast(self, message, client=None):
    for c in self.clients:
      if c != client:
        try:
          c.send(message)
        except:
          self.remove_client(c)

  def handle_client(self, client):
    while True:
      try:
        message = client.recv(1024)
        if b'\n' in message:
          header, file_data = message.split(b'\n', 1)
          header = header.decode('ascii')
          nickname, file_info = header.split(': ', 1)
          file_type, file_name, file_size = file_info.split(' ', 2)
          file_size = int(file_size)

          if file_size > 4 * 1024 * 1024:  # 4MB
            self.broadcast("File size exceeds the maximum limit of 4MB.".encode('ascii'))
            return

          remaining_data = file_size - len(file_data)
          while remaining_data > 0:
            chunk = client.recv(min(remaining_data, 1024))
            file_data += chunk
            remaining_data -= len(chunk)

          self.save_file(file_data, file_type, file_name)
          self.broadcast(f"{nickname} sent a {file_type} file: {file_name}".encode('ascii'), client)
        else:
          self.broadcast(message, client)
      except:
        self.remove_client(client)
        break

  def save_file(self, file_data, file_type, file_name):
    script_dir = os.path.dirname(__file__)
    uploads_dir = os.path.join(script_dir, '..', 'uploads', file_type)
    os.makedirs(uploads_dir, exist_ok=True)
    base_name, extension = os.path.splitext(file_name)
    file_path = os.path.join(uploads_dir, file_name)

    index = 1
    while os.path.exists(file_path):
      new_file_name = f"{base_name}({index}){extension}"
      file_path = os.path.join(uploads_dir, new_file_name)
      index += 1

    with open(file_path, 'wb') as file:
      file.write(file_data)

    print(f"Saved {file_type} file: {os.path.basename(file_path)}")

  def remove_client(self, client):
    if client in self.clients:
      index = self.clients.index(client)
      self.clients.remove(client)
      client.close()
      nickname = self.nicknames.pop(index)
      self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
      print(f'{nickname} has disconnected.')

  def receive(self):
    while True:
      client, address = self.server.accept()
      print(f'Connected with {str(address)}')

      client.send('NICK'.encode('ascii'))
      nickname = client.recv(1024).decode('ascii')
      self.nicknames.append(nickname)
      self.clients.append(client)

      print(f'Nickname of client is {nickname}!')
      self.broadcast(f'{nickname} joined the chat!'.encode('ascii'))
      client.send('Connected to the server!'.encode('ascii'))

      thread = threading.Thread(target=self.handle_client, args=(client,))
      thread.start()
