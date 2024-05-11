# 
# client_screen.py
#
# Name: Pedro Botelho
# Date: 20/03/2024
#

import PySimpleGUI as sg

class ClientScreen:
    def __init__(self):
        sg.theme('DarkAmber')
        self.layout = [[sg.Multiline(size=(50, 20), key='inbox', write_only=True, disabled=True)],
                       [sg.Multiline(size=(43, 1), key='input', no_scrollbar=True, rstrip=True, enter_submits=True), sg.Button('Send', bind_return_key=True)]]
        self.window = sg.Window('MySpace++', self.layout).Finalize()
        self.event, self.values = (0, 0)

    def write_inbox(self, message):
        self.window['inbox'].update(message+'\n', append=True)

    def read_input(self):
        message = self.values['input']
        self.window['input'].update('')
        return message

    def update_event(self):
        self.event, self.values = self.window.read(timeout=100)

    def check_close_event(self):
        return self.event == sg.WIN_CLOSED

    def check_send_event(self):
        if self.event == 'Send':
            self.event = 0
            return True
        return False

    def set_title(self, new_title):
        self.window.set_title(new_title)
    
    def close(self):
        self.window.close()

    def popup_ok(self, message):
        sg.popup_ok(message, title="MySpace++", non_blocking=True)

    def popup_error(self, message):
        sg.popup_error(message)
    