import socket
import tqdm

# Bind to all interfaces
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))

server.listen()
print("Waiting for connection...")
client, addr = server.accept()
print(f"Connected with {addr}")

filename = client.recv(1024).decode()
file_size = client.recv(1024).decode()

file = open(filename, 'wb')
file_bytes = b""
done = False

progress = tqdm.tqdm(total=int(file_size), unit='B', unit_scale=True, unit_divisor=1024)

while not done:
    data = client.recv(1024)
    if data.endswith(b"<END>"):
        done = True
        file_bytes += data[:-5]
    else:
        file_bytes += data
    progress.update(len(data))

file.write(file_bytes)
file.close()

client.close()
server.close()
