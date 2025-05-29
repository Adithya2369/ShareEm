# ShareEm

ShareEm is a terminal-based file sharing tool for fast, secure transfers over a local network—no internet needed. Inspired by apps like SHAREit and Xender, ShareEm uses socket programming for efficient LAN file exchange via the command line.

---

## Features

- 🚀 **Fast local file sharing** over LAN  
- 🔒 **Secure and private**: No internet required, files stay on your network  
- 🖥️ **Terminal-based**: Lightweight, no GUI required  
- ⚡ **Easy to use**: Simple commands for sending and receiving files

---

## Topics

- file-sharing
- terminal
- LAN
- socket-programming
- command-line
- networking

---

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- All devices must be connected to the same local network

### Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/Adithya2369/ShareEm.git
    cd ShareEm
    ```

2. **(Optional) Create a virtual environment:**
    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

---

## Usage

### 1. Start the Receiver

On the receiving device, run:
```
python receiver.py
```
The receiver will wait for incoming files.

### 2. Send a File

On the sending device, run:
```
python sender.py <receiver_ip> <file_path>
```
Replace `<receiver_ip>` with the IP address of the receiver, and `<file_path>` with the path to the file you want to send.

**Example:**
```
python sender.py 192.168.1.5 myphoto.jpg
```

---

## Notes

- Ensure both devices are on the same Wi-Fi or LAN network.
- Large files may take some time depending on your network speed.
- For best results, disable firewalls that may block local connections.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.

---

## Credits

Inspired by SHAREit and Xender.

---

**Happy Sharing! 🚀**
