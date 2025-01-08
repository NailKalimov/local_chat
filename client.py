from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import messagebox
import json

with open('config.json') as json_file:
    config = json.load(json_file)


def receive():
    while True:
        try:
            msg = CLIENT.recv(BUFSIZ).decode("utf8")
            n = 60
            for i in range(0, len(msg), n):
                msg_list.insert(tk.END, msg[i:(i + n)])

        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    msg = my_msg.get()

    my_msg.set('')  # Clears input field.
    CLIENT.send(bytes(msg, 'utf8'))


def on_closing(event=None):
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        my_msg.set('{quit}')
        send()
        CLIENT.close()
        root.quit()


# Создадим окно программы, а в нем поле, в котором
# будут отображаться сообщения, поле для ввода и кнопка:
root = tk.Tk()
root.title('Chat')
root.geometry('450x400')
# root.resizable(False, False)


messages_frame = tk.Frame(root)
my_msg = tk.StringVar()
scrollbar = tk.Scrollbar(messages_frame)

msg_list = tk.Listbox(messages_frame, height=20, width=60, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
messages_frame.pack()

# С помощью метода tk.Entry() создается поле для
# ввода сообщений. Все содержимое этого поля будет записано в переменную my_msg. Но сообщение на сервер
# будет отправлено только после того, как пользователь
# нажмет кнопку Send, то есть выполнится команда send
entry_field = tk.Entry(root, width=62, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tk.Button(root, text="Send", width=15, command=send)
send_button.pack()

# Если клиент решит закрыть окно, то появится диалоговое окно с просьбой подтвердить выход из программы on_closing():
root.protocol("WM_DELETE_WINDOW", on_closing)

# Затем инициализируем переменные, подключение к
# серверу и главное окно программы:
HOST = config['ip']
PORT = config['port']
BUFSIZ = 1024
ADDR = (HOST, PORT)
CLIENT = socket(AF_INET, SOCK_STREAM)
CLIENT.connect(ADDR)

# Вновь обращаемся к модулю threading и запускаем
# главный цикл программы:
RECEIVE_THREAD = Thread(target=receive)
RECEIVE_THREAD.start()
root.mainloop()
