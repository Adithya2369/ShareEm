# How to run:
# python sender.py --ip <receiver_ip_address> <file1> <file2> ...
# 192.168.70.245
# Example: python sender.py --ip 192.168.1.100 file1.txt file2.pdf
# Note: Multiple files can be specified at once

import os
import socket
import sys
import argparse
import time

def send_file(client, file_path):
    try:
        file = open(file_path, "rb")
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)

        # Ensure filename is safe to encode
        try:
            filename.encode('utf-8')
        except UnicodeEncodeError:
            print(f"Error: Filename {filename} contains invalid characters")
            return False

        # Send filename and size with delimiters
        # Use the last | as the separator between filename and size
        header = f"{filename}|{file_size}||".encode('utf-8')
        client.send(header)

        # Send file data in chunks
        CHUNK_SIZE = 1024
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            client.send(chunk)
        
        # Send end marker with a small delay to ensure proper separation
        time.sleep(0.1)  # Small delay to ensure proper separation
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
        client.send(f"{len(args.files)}||".encode())
        
        # Send each file
        for file_path in args.files:
            if not send_file(client, file_path):
                break
        
        client.close()
    except Exception as e:
        print(f"Connection error: {str(e)}")

if __name__ == "__main__":
    main()
