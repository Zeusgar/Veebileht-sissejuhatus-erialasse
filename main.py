import http.server
import os
import socketserver
import threading
import webbrowser

PORT = 8000

# Serveeri faile sellest kaustast, kus see .py fail asub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Kasitleja(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Ära hoia vanu faile vahemälus, et muudatused oleks kohe näha
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def leia_vaba_port(algus):
    port = algus
    while True:
        try:
            server = socketserver.TCPServer(("127.0.0.1", port), Kasitleja)
            return server, port
        except OSError:
            port += 1


def main():
    server, port = leia_vaba_port(PORT)
    aadress = f"http://localhost:{port}/index.html"

    print(f"Veebileht töötab: {aadress}")
    print("Peatamiseks vajuta Ctrl + C")

    # Ava brauser pool sekundit hiljem, kui server juba käib
    threading.Timer(0.5, lambda: webbrowser.open(aadress)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer peatatud.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()