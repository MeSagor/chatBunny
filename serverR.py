import threading
import socket

# host = socket.gethostbyname(socket.gethostname())
host = '127.0.0.1'
port = 65433

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
banned = []
stopThreads = False
adminDeactivate = True


# admin operations handling
def admin_operations():
    while True:
        try:
            command = input()

            # Threads Clean up? kill
            global stopThreads
            if stopThreads:
                break

            if command == "ban":
                nick = input("Ban Nickname: ")
                for client in clients:
                    if nicknames[clients.index(client)] == nick:
                        client.sendall('        ----You Are Banned!!!\n'.encode('utf-8'))
                        broadcast(f"        ----{nick} is Banned!!!\n".encode('utf-8'))
                        banned.append(nick)
                        client.close()
                        break
            elif command == "clients":
                print(nicknames)
        except:
            print("Input Command Error !!!")
            break


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.sendall(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)

            # Threads Clean up? kill
            global stopThreads
            if stopThreads:
                break

            broadcast(message)
        except:
            # Removing And Closing Clients
            print("Client removed !!!")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('        ----{} left!\n'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        global adminDeactivate
        if adminDeactivate:
            print(f"[SERVER RUNNING]...")
        else:
            print(f"[SERVER RUNNING WITH ADMIN]...")

        try:
            # Accept Connection
            (client, address) = server.accept()
            print("[CONNECTED]: {}".format(str(address)))
            # Request And Store Nickname
            nickname = client.recv(1024).decode('utf-8')

            # Check if nickname is in Banned list
            nickBanned = False
            for nick in banned:
                if nick == nickname:
                    nickBanned = True
                    client.sendall('        ----You Are Banned previously!!!\n'.encode('utf-8'))
                    client.close()
                    break
            if nickBanned:
                continue

            nicknames.append(nickname)
            clients.append(client)

            # Print And Broadcast Nickname
            print("[NICKNAME]: {}".format(nickname))
            client.sendall('Connected to server!\n'.encode('utf-8'))
            broadcast("        ----{} joined!\n".format(nickname).encode('utf-8'))

            # Start Handling Thread For Client
            threading.Thread(target=handle, args=(client,)).start()
            if adminDeactivate:
                threading.Thread(target=admin_operations).start()
                adminDeactivate = False

            print(f"[TOTAL USER]: {threading.active_count() - 2}")

        except:
            global stopThreads
            stopThreads = True
            server.close()
            print("[SERVER CLOSED]...")
            exit(0)
            break


print(f"[SERVER STARTING]...")
receive()
