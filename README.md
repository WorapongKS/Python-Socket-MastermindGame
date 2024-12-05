# Python-Socket-MastermindGame

  This project was developed by me and my university teammates as part of a course, utilizing socket programming to create a multiplayer Mastermind game. The game allows multiple players to connect to a server and take turns guessing a 6-digit secret code, with real-time feedback provided after each guess.

## Features
- Multiplayer Support: 2-5 players can connect to the server and play.
- Turn-Based Gameplay: Players take turns guessing the secret code.
- Guess Validation: The server checks the guess and provides feedback on the number of correct digits in the correct position and in any position.
- Game End Conditions: The game ends when a player guesses correctly or the maximum number of guesses is reached.
- Real-Time Interaction: Sockets and threading are used to enable communication between clients and the server in real-time.

## Technologies Used
- Python: The main programming language used to develop the game.
- Socket Programming: Used to establish client-server communication for multiplayer gameplay.
- Threading: Allows multiple clients to connect and play the game simultaneously.
- Random: Used to generate the 6-digit secret code for the game.

# How the Game Works


## Server
- The server listens for incoming connections from players and manages the game.
- Once the required number of players (2-5) is connected, the game begins.
- The server validates each guess and provides feedback to the player about the correctness of their guess (correct digits in the right position and correct digits in any position).
- The game continues until a player guesses the secret code or the maximum number of guesses is reached.

## Client
- Players run the client on their machine to connect to the server.
- Once connected, players will receive instructions and take turns guessing the secret code.
- After each guess, the server sends feedback on how many digits are correct and in the correct position, helping the player refine their next guess.
- Players continue until someone guesses the correct code or the game ends.
