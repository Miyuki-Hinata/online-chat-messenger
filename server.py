import socket

def udp_chat_server(host='127.0.0.1', port=12345):
    # Create a new UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Associates the socket with the host and port, making the server listen for incoming data on this address.
    server_socket.bind((host, port))

    # An empty set to store the addresses of all clients that connect to the server.
    clients = set()
    
    print(f"Server started on {host}:{port}. Waiting for clients...")

    while True:

        # The server waits for a message from any client using the recvfrom method. It receives up to 4096 bytes of data and also gets the address (addr) of the sender.
        data, addr = server_socket.recvfrom(4096)
        if addr not in clients:
            clients.add(addr)

        # The server waits for a message from any client using the recvfrom method. It receives up to 4096 bytes of data and also gets the address (addr) of the sender.
        username_len = data[0]

        # The next portion of the data contains the username. We slice the data starting from index 1 (just after the first byte) up to username_len + 1 (the end of the username). It’s then decoded from bytes into a string (utf-8 format).
        username = data[1:username_len + 1].decode('utf-8')

        # The remainder of the data after the username is the actual message, which is also decoded from bytes to a string.
        message = data[username_len + 1:].decode('utf-8')
        
        print(f"Received message from {username}: {message}")
        
        # Relay the message to all other clients
        for client in clients:
            # Except the original sender.
            if client != addr:
                server_socket.sendto(data, client)

if __name__ == '__main__':
    udp_chat_server()
