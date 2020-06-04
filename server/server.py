from http.server import BaseHTTPRequestHandler, HTTPServer


# noinspection PyPep8Naming
class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("received get request \n".encode('utf_8'))

    def do_POST(self):
        self._set_headers()
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len).decode('utf_8')
        self.wfile.write("received post request:<br>{} \n".format(post_body).encode('utf_8'))

    def do_PUT(self):
        self.do_POST()


host = ''
port = 80
HTTPServer((host, port), HandleRequests).serve_forever()
