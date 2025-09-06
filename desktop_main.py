import threading
import time
import socket
import webview
from app import app

HOST = "127.0.0.1"
PORT = 8992

def run_flask():
    app.run(host=HOST, port=PORT, debug=False)

def wait_for_server(host, port, timeout=5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            s = socket.create_connection((host, port), timeout=0.5)
            s.close()
            return True
        except Exception:
            time.sleep(0.1)
    return False

if __name__ == "__main__":
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    if not wait_for_server(HOST, PORT, timeout=8.0):
        time.sleep(1)

    webview.create_window("Text Navigator", f"http://{HOST}:{PORT}")
    webview.start()