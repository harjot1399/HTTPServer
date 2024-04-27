#!/usr/bin/env python3

"""
A basic Python 3 HTTP/1.1 server.
"""

import socketserver
import pathlib

HOST = "0.0.0.0"
PORT = 8000
BUFSIZE = 4096
LINE_ENDING = '\r\n'
SERVE_PATH = pathlib.Path('www').resolve()
HTTP_1_1 = 'HTTP/1.1'
METHOD_NOTALLOWED = ["POST", "PUT", "DELETE"]
RESPONSE_405 = HTTP_1_1 + " 405 Method Not Allowed"
HEADER_HTML = "Content-Type: text/html"
HEADER_CSS = "Content-Type: text/css"
RESPONSE_OK = HTTP_1_1 + " 200 OK"
RESPONSE_301 = HTTP_1_1 + " 301 Moved Permanently"
RESPONSE_404 = HTTP_1_1 + " 404 Not Found"


class LabServer(socketserver.TCPServer):
    allow_reuse_address = True


class LabServerTCPHandler(socketserver.StreamRequestHandler):
    def __init__(self, *args, **kwargs):
        self.charset = "UTF-8"
        self.serve_path = pathlib.Path("www").resolve()
        super().__init__(*args, **kwargs)

    def recieve_line(self):
        return self.rfile.readline().strip().decode(self.charset, 'ignore')

    def send_line(self, line):
        self.wfile.write((line + LINE_ENDING).encode(self.charset, 'ignore'))

    def send_file(self, line):
        self.wfile.write(line.encode(self.charset, 'ignore'))

    def method_check(self, method):
        if method in METHOD_NOTALLOWED:
            return True
        return False

    def read_content(self, path):
        with open(path, 'r') as x:
            lines = x.readlines()
            for line in lines:
                self.send_file(line)


    def handle(self):
        start_line = self.recieve_line()
        response = start_line.split()
        method = response[0]
        path = response[1]
        complete_path = (pathlib.Path('www' + path)).resolve()
        
        if self.method_check(method):
            self.send_line(RESPONSE_405)
        
        if complete_path.exists():
            
            if path[-1] == '/':
                file_html = "index.html"
                file_path = complete_path / file_html
                if file_path.exists():
                    self.send_line(RESPONSE_OK)
                    self.send_line(HEADER_HTML)
                    self.send_line('')
                    self.read_content(file_path)
            else:
                if SERVE_PATH in complete_path.parents:
                    if complete_path.is_file():
                        file_name = complete_path.name
                        self.send_line(RESPONSE_OK)
                        file_type = file_name.split('.')
                        if file_type[1] == "html":
                            self.send_line(HEADER_HTML)
                            self.send_line('')
                            self.read_content(complete_path)
                        else:
                            self.send_line(HEADER_CSS)
                            self.send_line('')
                            self.read_content(complete_path)

                    elif complete_path.is_dir():
                        dir_name = complete_path.name
                        self.send_line(RESPONSE_301)
                        new_dir = dir_name + "/"
                        new_location = "Location: " + new_dir
                        self.send_line(new_location)
                else:
                    self.send_line(RESPONSE_404)
                
        else:
            self.send_line(RESPONSE_404)
        



def main():
    # From https://docs.python.org/3/library/socketserver.html, The Python Software Foundation, downloaded 2024-01-07
    with LabServer((HOST, PORT), LabServerTCPHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()