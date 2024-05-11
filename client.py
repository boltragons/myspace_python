# 
# client.py
#
# Name: Pedro Botelho
# Date: 20/03/2024
#

import socket
import threading
import sys

from client_screen import ClientScreen
import tkthread

show_ok_popup = False

screen = ClientScreen()

# Choosing Nickname
screen.write_inbox("Welcome to MySpace++!\nChoose your nickname:");

while True:
    screen.update_event()

    if screen.check_send_event():
        break
    if screen.check_close_event():
        screen.close()
        sys.exit(0)
        break

nickname = screen.read_input()

screen.set_title('MySpace++ [{}]'.format(nickname))

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55500))

# Listening to Server and Sending Nickname
def receive():
    global show_ok_popup
    while True:
        if screen.check_close_event():
            break;
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            elif message == 'WELCOME':
                show_ok_popup = True
                # screen.write_inbox('Connected to server! Welcome.')
            else:
                screen.write_inbox(message)

        except RuntimeError as error:
            # tkthread.call_nosync(screen.popup_error, 'A fatal error occurred! Exiting.')
            print("An error occured!\n[error] ", error)
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        if screen.check_close_event():
            break;
        elif screen.check_send_event():
            message = '{}: {}'.format(nickname, screen.read_input())
            client.send(message.encode('utf-8'))
            
    client.send('EXIT'.encode('utf-8'))
    client.shutdown(0)

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

while True:
    screen.update_event()
    if screen.check_close_event():
        break
    if show_ok_popup:
        screen.popup_ok('Connected to server! Welcome.')
        show_ok_popup = False

while receive_thread.is_alive() or write_thread.is_alive():
    continue

screen.close()
