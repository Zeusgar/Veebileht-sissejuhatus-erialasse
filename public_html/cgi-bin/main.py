import os
from html import escape
from urllib.parse import parse_qs

params = parse_qs(os.environ.get("QUERY_STRING", ""))
nimi = escape(params.get("nimi", ["Külaline"])[0])

print("Content-Type: text/html; charset=utf-8")
print()
print(f"<h1>Tere, {nimi}!</h1>")