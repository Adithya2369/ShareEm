import os
import socket
import sys
import argparse

def send_file(client, file_path):
    try:
        file = open(file_path, "rb")
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)

        # Send filename and size
        client.send(filename.encode())
        client.send(str(file_size).encode())

        # Send file data
        data = file.read()
        client.sendall(data)
        client.send(b"<END>")

        file.close()
        print(f"Successfully sent {filename}")
        return True
    except Exception as e:
        print(f"Error sending {file_path}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Send files to a receiver')
    parser.add_argument('--ip', required=True, help='IP address of the receiver')
    parser.add_argument('files', nargs='+', help='Files to send')
    args = parser.parse_args()

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((args.ip, 9999))
        
        # Send number of files first
        client.send(str(len(args.files)).encode())
        
        # Send each file
        for file_path in args.files:
            if not send_file(client, file_path):
                break
        
        client.close()
    except Exception as e:
        print(f"Connection error: {str(e)}")

if __name__ == "__main__":
    main()
