import socket
import threading
import tkinter
from tkinter import ttk
import tkinter.scrolledtext
from tkinter import Button, Frame, simpledialog
from PIL import Image, ImageTk
import tkinter.font as tkfont

window = tkinter.Tk()
window.title("Simple Chat")
window.geometry("400x600")
window.configure(bg='#0f1b24')
window.resizable(0, 0)

logo = Image.open("images/WeChat.png")
logo = logo.resize((300, 200))
logo = ImageTk.PhotoImage(logo)

label = tkinter.Label(window, image=logo, bg="#0f1b24")
label.place(x=50, y=100)

#IP ADDRESS
ip_address_label = tkinter.Label(window, text="IP ADDRESS", font=("Arial", 12, "bold"), bg="#0f1b24",fg="white", justify="center")
ip_address_label.place(x=152, y=320)

input_field = tkinter.Entry(window, width=20, font=("Times New Roman", 12,), justify="center")
input_field.place(x=122, y=350)

font= "Arial"
size= "10"

PORT = 12345

#Scene Setting
def toggle_win():
    f1 = Frame(window, width=300, height=600, bg='#284352')
    f1.place(x=0, y=0)

    def dele():
        f1.destroy()

    def on_button_ok():
        global font, size
        font = combo_box1.get()
        size = combo_box2.get()
        f1.destroy()

    global img2
    img2 = ImageTk.PhotoImage(Image.open("images/closeButton.png"))

    Button(f1,image=img2, border=0, command=dele, activebackground="#284352", width=30, height=30).place(x=5, y=10)

    label = tkinter.Label(f1, text="Settings", bg="#284352", font=("Arial", 25, "bold"))
    label.place(x=70, y=35)

    label1 = tkinter.Label(f1, text="Font", bg="#284352", font=("Arial", 10, "bold"))
    label1.place(x=50, y=100)

    # fonts = sorted(tkfont.families())
    combo_box1 = ttk.Combobox(f1, values=['Arial', 'Times New Roman', 'Calibri', 'Courier New', 'Georgia', 'Roboto'])
    combo_box1.place(x=100, y=100)   

    label2 = tkinter.Label(f1, text="Size", bg="#284352", font=("Arial", 10, "bold"))
    label2.place(x=50, y=130)

    combo_box2 = ttk.Combobox(f1, values=['8', '10', '12', '14'])
    combo_box2.place(x=100, y=130)  

    button = tkinter.Button(f1, text="OK", command=on_button_ok, bg="#347295", fg="white", width=5, height=1,
                        font=("Arial", 10, "bold"))
    button.config(font=("Arial", 12))
    button.place(x=100, y= 160)

img1 = ImageTk.PhotoImage(Image.open("images/open.png"))

button = Button(window, image=img1, command=toggle_win, border=0, bg='#262626', activebackground='#262626').place(x=5, y=10)

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        if self.nickname:
            self.gui_done = False
            self.running = True

            gui_thread = threading.Thread(target=self.chat_scene)
            receive_thread = threading.Thread(target=self.receive)

            gui_thread.start()
            receive_thread.start()
        else:
            self.sock.close()

    def chat_scene(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="#284352")
        self.win.minsize(400, 600)
        self.win.maxsize(400, 600)

        self.chat_label = tkinter.Label(self.win, text="SimpleChat", bg="#0f1b24", fg="white", width=100, height=2)
        self.chat_label.config(font=("Comic Sans MS", 20 , "bold"))
        self.chat_label.pack(padx=0, pady=0)

        if int(size) == 8:
            height = 25
        elif int(size) == 10:
            height = 21
        elif int(size) == 12:
            height = 17
        elif int(size) == 14:
            height = 15        

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win,font=(font, size, "bold"), height=height)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.config(state='disabled')

        self.chat_label = tkinter.Label(self.win, text=self.nickname ,bg="#284352", fg="#FFFFFF", height=1)
        self.chat_label.config(font=("Comic Sans MS", 13 , "bold"))
        self.chat_label.pack(padx=5, pady=5)

        if int(size) == 8:
            width = 47
        elif int(size) == 10:
            width = 40
        elif int(size) == 12:
            width = 33
        elif int(size) == 14:
            width = 27

        self.input_area = tkinter.Text(self.win, height=2, width=width, font=(font, size, "bold"))
        self.input_area.pack(padx=15, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.send_message, bg="#347295", fg="white", width=7, height=1,
                        font=("Arial", 10, "bold"))
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=10, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def send_message(self):
        message = self.input_area.get("1.0", "end").strip()  
        if message:
            self.write(message)

    def write(self, message):
        message = f"{self.nickname}: {message}\n"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete("1.0", "end")


    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', f"{message}\n")
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

def button_clicked():
    global HOST
    HOST = input_field.get()
    # client = Client(HOST, PORT)
    client = Client(HOST, PORT)
    window.destroy()

#Button Mulai
button = tkinter.Button(window, text="MULAI", command=button_clicked, bg="#347295", fg="white", width=10, height=2,
                        font=("Arial", 10, "bold"))
button.place(x=160, y=420)

window.mainloop()