# 
# server.py
#
# Name: Pedro Botelho
# Date: 20/03/2024
#

import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55500

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if(message == 'EXIT'.encode('utf-8')):
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('utf-8'))
                nicknames.remove(nickname)
                break
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} boomed out!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
while True:
    # Accept Connection
    client, address = server.accept()
    print("Connected with {}".format(str(address)))

    # Request And Store Nickname
    client.send('NICK'.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    nicknames.append(nickname)
    clients.append(client)

    # Print And Broadcast Nickname
    print("Nickname is {}".format(nickname))
    broadcast("{} joined!".format(nickname).encode('utf-8'))
    client.send('WELCOME'.encode('utf-8'))

    # Start Handling Thread For Client
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()
