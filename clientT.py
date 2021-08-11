import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

# host = socket.gethostbyname(socket.gethostname())
host = '127.0.0.1'
port = 65433


# Connecting To Server
class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
        except:
            print("Can't connect to the host !!!!\nPlease check the host ip and port number.")
            exit(0)

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
        self.sock.sendall(self.nickname.encode('utf-8'))

        def write():
            message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
            print("Client sending massage")
            try:
                self.sock.sendall(message.encode('utf-8'))
            except:
                print("Connection Error")
            self.input_area.delete('1.0', 'end')

        def stop():
            self.running = False
            self.win.destroy()
            self.sock.close()
            exit(0)

        self.gui_done = False
        self.running = True

        # Data mining Thread Starting...
        threading.Thread(target=self.receiveData).start()

        self.win = tkinter.Tk(className=f"chatBunny({self.nickname})")
        self.win.minsize(500, 450)
        self.win.maxsize(650, 500)
        self.win.configure(bg="lightgray")
        #
        chatLabel = tkinter.Label(self.win, text="Chat:")
        chatLabel.config(font=("Arial", 12))
        chatLabel.pack(padx=20, pady=5)
        chatLabel.configure(bg="lightgray")
        #
        self.textArea = tkinter.scrolledtext.ScrolledText(self.win)
        self.textArea.pack(padx=20, pady=5)
        self.textArea.configure(state='disabled')
        #
        msgLable = tkinter.Label(self.win, text="Message")
        msgLable.config(font=("Arial", 12))
        msgLable.configure(bg="lightgray")
        msgLable.pack(padx=20, pady=5)
        #
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)
        #
        sendButton = tkinter.Button(self.win, text="Send", width=12, height=2, command=write)
        sendButton.config(font=("Arial", 12))
        sendButton.configure(bg="lightgray")
        sendButton.pack(padx=20, pady=5)
        #
        self.win.protocol("WM_DELETE_WINDOW", stop)

        self.gui_done = True

        self.win.mainloop()

    def receiveData(self):
        while self.running:
            if self.gui_done:
                try:
                    print("Client getting message & broadcasting it")
                    message = self.sock.recv(1024).decode('utf-8')
                    if len(message) == 0:
                        break
                    else:
                        self.textArea.configure(state='normal')
                        self.textArea.insert('end', message)
                        self.textArea.yview('end')
                        self.textArea.configure(state='disabled')

                except:
                    print("Connection Error Or left")
                    self.sock.close()
                    break


client = Client(host, port)
