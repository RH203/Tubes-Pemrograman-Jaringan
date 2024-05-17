import socket
import threading
import os


class ChatServer:
  def __init__(self, host='0.0.0.0', port=5555):
    '''
    Inisialisasi objek ChatServer dan mengikat server socket ke alamat dan port yang ditentukan.

    Parameter:
        - host: Alamat IP yang akan diikat oleh server.
        - port: Nomor port yang akan digunakan oleh server.
    '''
    self.host = host
    self.port = port
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((host, port))
    self.server.listen()
    self.clients = []
    self.nicknames = []

  def broadcast(self, message, client=None):
    '''
    Fungsi ini akan mengirim pesan kepada semua client kecuali client yang melakukan pengiriman pesan.

    Parameter:
        - message: Pesan yang akan dikirim.
        - client: Socket client yang sedang mengirim pesan. Jika tidak ditentukan, pesan akan dikirim ke semua client.
    '''
    for c in self.clients:
      if c != client:
        try:
          c.send(message)
        except:
          self.remove_client(c)

  def handle_client(self, client):
    '''
    Fungsi ini akan menangani komunikasi antara server dan client, menerima pesan dari client, memprosesnya, dan menyebarkannya.

    Parameter:
        - client: Socket client yang sedang aktif.
    '''
    while True:
      try:
        message = client.recv(1024)
        if b'\n' in message:
          header, file_data = message.split(b'\n', 1)
          header = header.decode('ascii')
          nickname, file_info = header.split(': ', 1)
          file_type, file_name, file_size = file_info.split(' ', 2)
          file_size = int(file_size)

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
    '''
    Fungsi ini akan menyimpan file yang diterima dari client ke direktori yang sesuai di server, terdapat condition untuk
    menghindari konflik nama jika ada.

    Parameter:
        - file_data: Data file yang diterima dari client.
        - file_type: Jenis file yang diterima (audio, image, atau video).
        - file_name: Nama file yang diterima dari client.
    '''
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
    '''
    Fungsi ini akan menghapus client yang terputus dari daftar client yang terhubung ke server dan menutup soket client yang terputus.

    Parameter:
        - client: Socket client yang telah terputus.
    '''
    if client in self.clients:
      index = self.clients.index(client)
      self.clients.remove(client)
      client.close()
      nickname = self.nicknames.pop(index)
      self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
      print(f'{nickname} has disconnected.')

  def receive(self):
    '''
    Fungsi ini akan menerima koneksi baru dari client, menambahkan client ke daftar client yang terhubung, dan memulai
    thread baru untuk menangani koneksi tersebut.
    '''
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

