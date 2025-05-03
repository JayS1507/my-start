# 🕵️‍♂️ ShadowTrace: Keylogger & Mouse Logger with Reverse Shell

![Python](https://img.shields.io/badge/Python-3.7%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Educational%20Project-orange)

**ShadowTrace** is an advanced Python project designed for educational purposes, showcasing real-time keyboard and mouse event logging with a reverse shell to transmit logs to a remote server. Dive into the world of network programming, input monitoring, and ethical hacking concepts—all within a controlled, ethical environment.

⚠️ **Ethical Usage Warning**: This project is for **educational purposes only**. Do not use it to harm systems or networks without explicit permission. Unauthorized use of keyloggers or reverse shells is illegal and unethical.

## 🚀 Features

- **Real-Time Input Capture**: Logs keyboard keystrokes (alphanumeric and special keys) and mouse events (movements, clicks, scrolls) with precise timestamps.
- **Reverse Shell Transmission**: Sends logs (`keylog.txt` and `mouselog.txt`) to a remote server over TCP every 5 seconds.
- **Client-Server Design**: Includes a client (`client.py`) for logging events and a server (`server.py`) for receiving and storing logs.
- **Verbose Logging**: Both client and server provide detailed logs for debugging and monitoring.
- **Network Reachability Check**: Client tests server availability using `ping` before sending logs.
- **Cross-Platform Support**: Compatible with Windows, macOS, and Linux (with proper permissions).

## 🎯 Use Cases

- **Network Programming**: Learn client-server communication using Python’s `socket` library.
- **Input Monitoring**: Understand how to capture and process keyboard and mouse events with `pynput`.
- **Ethical Hacking Education**: Explore keylogging and reverse shell techniques in a controlled environment (e.g., penetration testing labs).
- **System Monitoring**: Monitor user activity on a system (with explicit consent).

## 📋 Prerequisites

- **Python 3.7+**: Ensure Python is installed on both client and server machines.
- **pynput Library**: For capturing keyboard and mouse events.
- **Network Access**: Client and server must be on the same network, with port `4444` open on the server.

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/[YourGitHubUsername]/ShadowTrace.git
   cd ShadowTrace
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Server IP**:
   - Open `client.py` and update `SERVER_IP` to your server’s IP address (default: `192.168.1.73`).
   - Example: If your server’s IP is `192.168.1.100`, set `SERVER_IP = "192.168.1.100"`.

## 🚀 Usage

1. **Run the Server**:
   - On the server machine (`192.168.1.73` or your configured IP), run:
     ```bash
     python server.py
     ```
   - The server will listen on `0.0.0.0:4444` for incoming connections.
   - Logs will be saved to `server_keylog.txt` and `server_mouselog.txt`.

2. **Run the Client**:
   - On the client machine, run:
     ```bash
     python client.py
     ```
   - Perform actions (type, move the mouse, click).
   - The client logs events to `keylog.txt` and `mouselog.txt` and sends them to the server every 5 seconds.
   - Press `Esc` to stop the client.

3. **Verify Logs**:
   - On the client: Check `keylog.txt` and `mouselog.txt` for local logs.
   - On the server: Check `server_keylog.txt` and `server_mouselog.txt` for received logs.

## 📄 Example Output

### Client Output
```
[2025-04-25 14:30:45] Starting key/mouse logger
[2025-04-25 14:30:45] Alphanumeric key h pressed
[2025-04-25 14:30:45] Updated keylog.txt with 1 entries
[2025-04-25 14:30:46] Testing network connectivity to 192.168.1.73
[2025-04-25 14:30:46] Ping successful: 192.168.1.73 is reachable
[2025-04-25 14:30:46] Connecting to 192.168.1.73:4444
[2025-04-25 14:30:46] Successfully connected to 192.168.1.73:4444
[2025-04-25 14:30:46] Sent keylog.txt: 30 bytes
```

### Server Output
```
[2025-04-25 14:30:45] Server listening on 0.0.0.0:4444...
[2025-04-25 14:30:46] Connected by ('192.168.1.100', 12345)
[2025-04-25 14:30:46] Saved keylog data from ('192.168.1.100', 12345): 30 bytes
[2025-04-25 14:30:46] Full data from ('192.168.1.100', 12345):
--- keylog.txt ---
[2025-04-25 14:30:45] h 
--- END ---
```

## ⚠️ Ethical Usage Disclaimer

This project is intended for **educational purposes only**. Keyloggers and reverse shells can be used to harm systems or networks if misused. **Do not use this software on any system without explicit permission**. Unauthorized use is illegal and unethical. The author is not responsible for any misuse or damage caused by this software.

## 🐞 Troubleshooting

- **Client Cannot Connect**:
  - Ensure the server is running before starting the client.
  - Verify `SERVER_IP` and `SERVER_PORT` in `client.py`.
  - Check firewall settings on the server:
    - Linux: `sudo ufw allow 4444`
    - Windows: Allow port `4444` in Windows Firewall.
  - Test connectivity: `ping 192.168.1.73` and `telnet 192.168.1.73 4444` from the client.

- **Log Files Not Generated**:
  - Perform actions (typing, mouse movement) to generate logs.
  - Check file permissions in the client’s working directory.

## 📝 Future Improvements

- Add encryption for secure log transmission.
- Implement authentication for server access.
- Throttle mouse movement logging to reduce data volume.
- Add a GUI for real-time log monitoring.

## 🤝 Contributing

Contributions are welcome! Open issues or submit pull requests to improve this project, ensuring alignment with ethical usage guidelines.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgements

- Built with [pynput](https://github.com/moses-palmer/pynput) for input monitoring.
- Inspired by educational resources on network programming and ethical hacking.

---

⭐ **Star this repository** if you found it helpful! Share your feedback or suggestions in the issues section.