import socket
import threading

def send_message(udp_socket, server_address, username):
  while True:
    message = input(f"{username}:")

    # The length of the username as a 1-byte integer. + The username, encoded as bytes. + The message, also encoded as bytes.
    data = len(username).to_bytes(1, 'big') + username.encode('utf-8') + message.encode('utf-8')

    # The client sends the constructed data to the server
    udp_socket.sendto(data, server_address)

def receive_message(udp_socket):
  while True:
    data, _ = udp_socket.recvfrom(4096)
    username_len = data[0]
    username = data[1:username_len + 1].decode('utf-8')
    message = data[username_len + 1].decode('utf-8')
    print(f"{username}: {message}")

def udp_chat_client(server_host='127.0.0.1', server_port=12345):
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server_address = (server_host, server_port)

  username = input("Enter your username: ")

  # Start sending and receiving threads
  # A new thread is started for the send_message function. This ensures that the user can continuously send messages without being blocked by receiving them.
  threading.Thread(target=send_message, args=(client_socket, server_address, username)).start()

  # Another thread is started for the receive_message function, allowing the client to continuously listen for incoming messages without being blocked by sending them.
  threading.Thread(target=receive_message, args=(client_socket,)).start()

if __name__ == '__main__':
  udp_chat_client()