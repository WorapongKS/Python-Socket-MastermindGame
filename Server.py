import socket
import random
import threading
from socket import * #Import all socket-related functions and constants for convenience

serverPort = 5000 #Set the server port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5) #Start listening for connections, allowing a maximum of 5 simultaneous connections

print('Waiting for players...')

#List to hold client sockets
clients = []
secretNumber = None
currentPlayer = 0
totalGuesses = 0
maxGuesses = 12
gameOver = False
minPlayers = 2
maxPlayers = 5

#Function to generate the secret number
def generateSecretNumber():
    digits = random.sample(range(10), 6)
    return ''.join(map(str, digits))

#Function to handle each player
def handle_client(connectionSocket, player_number):
    global currentPlayer, totalGuesses, gameOver
    
    while not gameOver: #Continue until the game is over
            if currentPlayer == player_number: #Check if it's this player's turn
                connectionSocket.send(f"It's your turn. Enter your guess (6 digits)".encode())
                guess = connectionSocket.recv(1024).decode().strip() #Wait for the player's guess
                
                #Validate the guess
                if len(guess) != 6 or not guess.isdigit():
                    connectionSocket.send("Invalid guess. Must be 6 digits.".encode())
                    continue
                
                totalGuesses += 1 #Increment the total number of guesses
                correctPos, correctDigits = check_guess(guess)#Check the guess
                response = f"{correctPos} {correctDigits} ({' '.join(guess)})"
                broadcast(f"Player {player_number + 1}'s guess (#{totalGuesses}): {response}")
                
                #Check if the player has won
                if correctPos == 6:
                    win_message = f"Player {player_number + 1} wins! The correct number was {secretNumber}"
                    broadcast(win_message)
                    print(f"{win_message}")
                    endGame(is_win=True)
                elif totalGuesses >= maxGuesses: #Check if the maximum number of guesses has been reached
                    endGame(is_win=False)
                else:
                    currentPlayer = (currentPlayer + 1) % len(clients) #Move to the next player
                    print(f"It's Player {currentPlayer + 1}'s turn.")
                    broadcast(f"It's Player {currentPlayer + 1}'s turn.")

#Function to check the guess
def check_guess(guess):
    correctPos = sum(g == s for g, s in zip(guess, secretNumber))
    correctDigits = sum(min(guess.count(d), secretNumber.count(d)) for d in set(guess)) - correctPos
    return correctPos, correctDigits

#Function to end the game
def endGame(is_win):
    global gameOver
    gameOver = True
    if is_win:
        
        pass
    else:
        end_message = f"Game over! The correct number was {secretNumber}."
        broadcast(end_message)
        print(end_message)
    
    #Wait for user input before closing the server
    input("Press Enter to close the server...")
       
#Function to broadcast messages to all players       
def broadcast(message):
    disconnected_clients = []
    for client in clients:
        try:
            client.send((message).encode()) #Send the message to the client
        except:
            disconnected_clients.append(client)
    
    for client in disconnected_clients:
        remove_client(client) #Remove disconnected clients

#Function to remove a client from the list
def remove_client(client):
    if client in clients:
        clients.remove(client)
        try:
            client.close() #Close the connection
        except:
            pass

#Function to start the game
def startGame():
    global secretNumber, gameOver, totalGuesses, currentPlayer
    secretNumber = generateSecretNumber()
    broadcast("Game starts!\n")
    gameOver = False
    totalGuesses = 0
    currentPlayer = 0
    
    print(f"It's Player {currentPlayer + 1}'s turn.")
    broadcast(f"It's Player {currentPlayer + 1}'s turn.") #Notify the current player's turn
    
    threads = []
    for i, client in enumerate(clients):
        thread = threading.Thread(target=handle_client, args=(client, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

#Function to accept connections from players
def accept_connections():
    while len(clients) < maxPlayers:
            
            connectionSocket, addr = serverSocket.accept()
            clients.append(connectionSocket)
            
            player_number = len(clients)
            print(f"Player {player_number} ({addr[0]}, {addr[1]}) has connected.")
            
            if len(clients) == minPlayers:
                print("Minimum players reached. Starting game immediately.")
                broadcast("Minimum players reached. Game starts now!")
                startGame()
                break
            elif len(clients) < minPlayers:
                broadcast(f"Waiting for more players. Current: {len(clients)}/{minPlayers}")
            elif len(clients) == maxPlayers:
                print("Maximum players reached. Starting game immediately.")
                broadcast("Maximum players reached. Game starts now!")
                startGame()
                break
      
if __name__ == "__main__":
        
        accept_connections()
        serverSocket.close()