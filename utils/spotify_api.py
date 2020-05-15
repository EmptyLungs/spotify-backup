import codecs
import json
import sys
import time
import webbrowser
import urllib.parse
import urllib.request

from utils.auth_server import AUTH_SERVER_HOST, AuthServer, SpotifyToken
from utils.logger import log

OAUTH_SPOTIFY_SCOPE = 'playlist-read-private'
OAUTH_SPOTIFY_CLIENT_ID = '8146ce078cfc47a78a8ec35f7f6533a1'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize?{}'


class SpotifyAPI(object):
    def __init__(self, client_token):
        self._token = client_token
        self._server_port = 43019
        self.spotify_root_url = 'https://api.spotify.com/v1/{}'

    @staticmethod
    def authorize():
        webbrowser.open(SPOTIFY_AUTH_URL.format(urllib.parse.urlencode({
            'response_type': 'token',
            'client_id': OAUTH_SPOTIFY_CLIENT_ID,
            'scope': OAUTH_SPOTIFY_SCOPE,
            'redirect_uri': f'http://127.0.0.1:{AUTH_SERVER_HOST[1]}/redirect'
        })))
        auth_server = AuthServer()
        try:
            while True:
                auth_server.handle_request()
        except SpotifyToken as auth:
            return SpotifyAPI(auth.token)

    def get(self, url, params=None, tries=3):
        if not url.startswith('https://api.spotify.com/v1/'):
            url = self.spotify_root_url.format(url)
        if params:
            url += '?' + urllib.parse.urlencode(params)
        for _ in range(tries):
            try:
                req = urllib.request.Request(url)
                req.add_header('Authorization', f'Bearer {self._token}')
                res = urllib.request.urlopen(req)
                reader = codecs.getreader('utf-8')
                return json.load(reader(res))
            except Exception as err:
                log(f'Error fetching api URL: {url, err}')
                time.sleep(1)
                log('Trying again')
        sys.exit(1)

    def list(self, url, params):
        resp = self.get(url, params)
        items = resp['items']
        while resp['next']:
            resp = self.get(resp['next'])
            items += resp['items']
        return items

