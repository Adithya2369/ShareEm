import socket
import tqdm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()
client, addr = server.accept()

filename = client.recv(1024).decode()
print(filename)
file_size = client.recv(1024).decode()
print(file_size)

file = open(filename, 'wb')

file_bytes = b""

done = False

progress = tqdm.tqdm(total=int(file_size), unit='B', unit_scale=True, unit_divisor=1024)

while not done:
    data = client.recv(1024)
    if data.endswith(b"<END>"):
        done = True
        file_bytes += data[:-5]  # exclude <END>
    else:
        file_bytes += data
    progress.update(1024)

file.write(file_bytes)

file.close()
client.close()
server.close()
