import socket
import tqdm
import os

def receive_file(client, progress_bar=None):
    try:
        # Receive filename and size
        filename = client.recv(1024).decode()
        file_size = client.recv(1024).decode()

        # Create downloads directory if it doesn't exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        
        file_path = os.path.join('downloads', filename)
        file = open(file_path, 'wb')
        file_bytes = b""
        done = False

        if progress_bar:
            progress = tqdm.tqdm(total=int(file_size), unit='B', unit_scale=True, unit_divisor=1024, desc=filename)
        else:
            progress = None

        while not done:
            data = client.recv(1024)
            if data.endswith(b"<END>"):
                done = True
                file_bytes += data[:-5]
            else:
                file_bytes += data
            if progress:
                progress.update(len(data))

        file.write(file_bytes)
        file.close()
        if progress:
            progress.close()
        print(f"Successfully received {filename}")
        return True
    except Exception as e:
        print(f"Error receiving file: {str(e)}")
        return False

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 9999))
        server.listen()
        print("Waiting for connection...")
        
        while True:
            client, addr = server.accept()
            print(f"Connected with {addr}")
            
            try:
                # Receive number of files
                num_files = int(client.recv(1024).decode())
                print(f"Receiving {num_files} files...")
                
                # Receive each file
                for i in range(num_files):
                    if not receive_file(client, progress_bar=True):
                        break
                
            except Exception as e:
                print(f"Error during transfer: {str(e)}")
            finally:
                client.close()
                print("Connection closed")
                
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    main()
