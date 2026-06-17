from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs

class MyHandler(SimpleHTTPRequestHandler):

    def do_POST(self):

        length = int(self.headers['Content-Length'])

        data = self.rfile.read(length).decode()

        form = parse_qs(data)

        username = form.get("username", [""])[0]
        password = form.get("password", [""])[0]

        if self.path == "/register":

            with open("users.txt", "a") as file:
                file.write(f"{username},{password}\n")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Registration Successful")

        elif self.path == "/login":

            valid = False

            try:
                with open("users.txt", "r") as file:

                    for line in file:
                        u, p = line.strip().split(",")

                        if u == username and p == password:
                            valid = True
                            break

            except FileNotFoundError:
                pass

            self.send_response(200)
            self.end_headers()

            if valid:
                self.wfile.write(b"Login Successful")
            else:
                self.wfile.write(b"Invalid Username or Password")


server = HTTPServer(("localhost", 8000), MyHandler)

print("Server running on http://localhost:8000")

server.serve_forever()