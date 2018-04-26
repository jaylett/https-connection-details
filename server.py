from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)
import json
import os
import ssl
import sys


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript")
        self.end_headers()
        response = {
            'cipher': self.request.cipher(),
            'compression': self.request.compression(),
            'selected_alpn_protocol': self.request.selected_alpn_protocol(),
            'selected_npn_protocol': self.request.selected_npn_protocol(),
            'session': {
                #'id': self.request.session.id,
                'timeout': self.request.session.timeout,
                'time': self.request.session.time,
                'ticket_lifetime_hint': self.request.session.ticket_lifetime_hint,
                'has_ticket': self.request.session.has_ticket,
            },
            #'shared_ciphers': self.request.shared_ciphers(),
            'version': self.request.version(),
        }
        self.wfile.write(json.dumps(response, indent=4).encode('utf-8'))


if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 4443), RequestHandler)
    if not os.path.exists('./server.pem'):
        sys.stderr.write("No server.pem file found! Please create one, eg:\n\n")
        sys.stderr.write(
            "openssl req -new -x509 -keyout server.pem -out "
            "server.pem -days 365 -nodes\n"
        )
        exit(1)

    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        certfile='./server.pem',
        server_side=True,
    )
    httpd.serve_forever()
