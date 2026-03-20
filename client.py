import socket

port = 12345

with socket.socket() as s:
    s.connect(("192.168.1.68", port))

    while True:
        string = input("Message to send: ")
        if string == "stop":
            s.shutdown(socket.SHUT_RDWR)
            break
        s.send(string.encode())
