import os, subprocess, sys
from http.server import SimpleHTTPRequestHandler, HTTPServer


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="public_html", **kwargs)

    def do_GET(self):
        if self.path.startswith("/cgi-bin/"):
            self.kaivita_skript()
        else:
            super().do_GET()

    def do_POST(self):
        self.kaivita_skript()

    def kaivita_skript(self):
        tee, _, parameetrid = self.path.partition("?")
        pikkus = int(self.headers.get("Content-Length") or 0)
        keskkond = dict(os.environ,
                        REQUEST_METHOD=self.command,
                        QUERY_STRING=parameetrid,
                        CONTENT_LENGTH=str(pikkus),
                        CONTENT_TYPE=self.headers.get("Content-Type", ""))

        tulemus = subprocess.run([sys.executable, "public_html" + tee],
                                 input=self.rfile.read(pikkus), env=keskkond,
                                 capture_output=True)
        print(tulemus.stderr.decode())

        paised, _, sisu = tulemus.stdout.replace(b"\r\n", b"\n").partition(b"\n\n")
        self.send_response(200)
        for rida in paised.decode().splitlines():
            nimi, _, vaartus = rida.partition(":")
            self.send_header(nimi, vaartus.strip())
        self.end_headers()
        self.wfile.write(sisu)


print("Ava http://localhost:8000/")
HTTPServer(("localhost", 8000), Handler).serve_forever()