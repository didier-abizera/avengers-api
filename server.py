import base64
import json 
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

USERS = {"admin": "secret", "driver": "pass123"}
AVENGERS = {
    "franchise": "Avengers",
    "movies": [
        "The Avengers",
        "Avengers: Age of Ultron",
        "Avengers: Infinity War",
        "Avengers: Endgame" 
    ],
}

def check_auth(header):
    if header is None:
        return False
    if not header.startswith("Basic "):
        return False 
    try:
        encoded = header[6:]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return USERS.get(username) == password
    except Exception:
        return False

class MovieHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data, extra_headers=None):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for name, value in extra_headers.items():
                self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)
    
    def do_GET(self):
        if not check_auth(self.headers.get("Authorization")):
            self.send_json(
                401,
                {"error": "Unauthorized"},
                {"WWW-Authenticate": 'Basic realm="Movies"'},
            )
            return 
        if self.path == "/movies/avengers":
            self.send_json(200, AVENGERS)
        else:
            self.send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    server = Threading(("0.0.0.0", 8000), MovieHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()