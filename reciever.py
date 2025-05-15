# How to run:
# python reciever.py
# Note: The receiver will listen on port 9999 on all network interfaces (0.0.0.0)
# Make sure this port is not blocked by firewall

import socket
import tqdm
import os

def receive_file(client, progress_bar=None):
    try:
        # Receive header info (filename and size)
        header = b""
        while b"||" not in header:
            chunk = client.recv(1024)
            if not chunk:
                break
            header += chunk
        
        if not header:
            return False
            
        # Split header and check for end marker
        header_parts = header.split(b"||")
        if len(header_parts) > 1 and header_parts[1].startswith(b"<END>"):
            # This was actually the end marker from previous file
            header = header_parts[0]
            # Get the next header
            next_header = b""
            while b"||" not in next_header:
                chunk = client.recv(1024)
                if not chunk:
                    break
                next_header += chunk
            header = next_header.split(b"||")[0]
        
        # Split the header into filename and size
        try:
            # Find the last occurrence of | to handle filenames that might contain |
            last_pipe = header.rfind(b"|")
            if last_pipe == -1:
                raise ValueError("Invalid header format: missing separator")
            
            filename = header[:last_pipe].decode('utf-8')
            file_size = int(header[last_pipe + 1:].decode('utf-8'))
            
            if not filename or file_size < 0:
                raise ValueError("Invalid filename or file size")
                
        except (UnicodeDecodeError, ValueError) as e:
            print(f"Error parsing header: {str(e)}")
            return False

        # Create downloads directory if it doesn't exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        
        file_path = os.path.join('downloads', filename)
        file = open(file_path, 'wb')
        bytes_received = 0
        CHUNK_SIZE = 1024

        if progress_bar:
            progress = tqdm.tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc=filename)
        else:
            progress = None

        # Receive file data in chunks
        while bytes_received < file_size:
            chunk = client.recv(min(CHUNK_SIZE, file_size - bytes_received))
            if not chunk:
                break
            file.write(chunk)
            bytes_received += len(chunk)
            if progress:
                progress.update(len(chunk))

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
                num_files_str = ""
                while "||" not in num_files_str:
                    num_files_str += client.recv(1024).decode()
                num_files = int(num_files_str.split("||")[0])
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
