import http.server
import urllib.parse

AUTH_SERVER_HOST = ('127.0.0.1', 43019)

class SpotifyToken(Exception):
    def __init__(self, token):
        self.token = token


class AuthHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/redirect'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<script>location.replace("token?" + location.hash.slice(1));</script>')

        elif self.path.startswith('/token?'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<script>close();</script> Close window now.')
            token = urllib.parse.parse_qs(self.path)['/token?access_token'][0]
            raise SpotifyToken(token)
        else:
            self.send_error(404)


class AuthServer(http.server.HTTPServer):
    def __init__(self):
        http.server.HTTPServer.__init__(self, AUTH_SERVER_HOST, AuthHandler)

    def handle_error(self, request, client_address):
        raise
