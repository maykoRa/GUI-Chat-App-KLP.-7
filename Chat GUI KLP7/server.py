import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345
print("IP Address: " + HOST)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []
    
def receive():
    while True:
        client, address = server.accept()
        print(f"Berhasil menghubungkan dengan {str(address)}!")
        
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname client yang terhubung : " + ", ".join(nicknames))
        broadcast(f"{nickname} bergabung ke dalam room chat!\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{message.decode('utf-8')}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} meninggalkan room chat!\n".encode('utf-8'))
            print(f"{nickname} meninggalkan room chat!\n")
            break
        
def broadcast(message):
    for client in clients:
        client.send(message)

print("Server running...")
receive()