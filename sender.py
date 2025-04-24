import os
import socket

# Replace with the actual IP of the receiving device
receiver_ip = "192.168.1.5"  # <-- change this
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((receiver_ip, 9999))

file = open("image.png", "rb")
file_size = os.path.getsize("image.png")

client.send("received_image.png".encode())
client.send(str(file_size).encode())

data = file.read()
client.sendall(data)
client.send(b"<END>")

file.close()
client.close()
