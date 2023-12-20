import socket
import threading

def send_message(client_socket):
    while True:
        message = input("Enter a message: ")
        client_socket.send(message.encode('utf-8'))

def receive_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            decoded_data = data.decode('utf-8')

            if decoded_data.startswith("Server: "):
                print(decoded_data)
            else:
                print(f"Received from server: {decoded_data}")

        except socket.error:
            # Handle errors if the server socket is no longer valid
            break

def main():
    host = 'your_ip_address'  # Replace with your actual IP address
    port = 12345  #select any port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

if __name__ == "__main__":
    main()
