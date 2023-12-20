import socket
import threading

# List to store connected client sockets
connected_clients = []

def handle_client(client_socket, client_address):
    # Add the client socket to the list of connected clients
    connected_clients.append(client_socket)

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received from {client_address}: {data.decode('utf-8')}")

            # Broadcast the message to all connected clients
            broadcast_message(data, sender=client_socket)
        except socket.error:
            # Handle errors if a client socket is no longer valid
            break

    # Remove the client socket when the connection is closed
    connected_clients.remove(client_socket)
    client_socket.close()

def broadcast_message(message, sender=None):
    # Broadcast the message to all connected clients
    for client in connected_clients:
        if client != sender:
            try:
                client.send(message)
            except socket.error:
                # Handle errors if a client socket is no longer valid
                connected_clients.remove(client)

def handle_server_input():
    # Separate thread for handling server input
    while True:
        message = input("Enter a message to broadcast to clients: ")
        broadcast_message(f"Server: {message}".encode('utf-8'))

def main():
    host = 'your_ip_address'  # Replace with your actual IP address
    port = 12345  #select any port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    # Start the thread for handling server input
    server_input_thread = threading.Thread(target=handle_server_input)
    server_input_thread.start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()