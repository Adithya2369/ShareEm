from flask import Flask, render_template, request, jsonify, send_file
import os
import socket
import threading
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024  # 16GB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def send_file_to_receiver(file_path, receiver_ip):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((receiver_ip, 9999))
        
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Send filename and size
        header = f"{filename}|{file_size}||".encode('utf-8')
        client.send(header)
        
        # Send file data in chunks
        CHUNK_SIZE = 1024
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(CHUNK_SIZE)
                if not chunk:
                    break
                client.send(chunk)
        
        # Send end marker
        time.sleep(0.1)
        client.send(b"<END>")
        client.close()
        return True
    except Exception as e:
        print(f"Error sending file: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files selected'}), 400
    
    receiver_ip = request.form.get('receiver_ip')
    if not receiver_ip:
        return jsonify({'error': 'Receiver IP not specified'}), 400
    
    files = request.files.getlist('files[]')
    results = []
    
    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Send file in a separate thread
            success = send_file_to_receiver(file_path, receiver_ip)
            
            # Clean up the uploaded file
            os.remove(file_path)
            
            results.append({
                'filename': filename,
                'success': success
            })
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 