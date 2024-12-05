import socket
from socket import *

def main():
    server_address = 'localhost'  # Replace with the server's address if needed
    server_port = 5000

    # Create a socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    
    
    # Connect to the server
    client_socket.connect((server_address, server_port))
    print("Connected to the server...")

    while True:
            # Receive messages from the server
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)

            # If it's a turn, get user input
            if "It's your turn" in message:
                guess = input("Enter your guess (6 digits): ")
                client_socket.send(guess.encode())

    
    client_socket.close()

if __name__ == "__main__":
    main()
