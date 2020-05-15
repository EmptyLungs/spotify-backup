import json

from utils.spotify_api import SpotifyAPI
from utils.logger import log

if __name__ == '__main__':
    api = SpotifyAPI.authorize()
    client = api.get(url='me')
    log("logged as {display_name} id: {id}".format(**client))
    playlists = api.list('me/playlists', {'limit': 50})
    for playlist in playlists:
        log('Loading playlist: {name} ({tracks[total]} songs)'.format(**playlist))
        playlist['tracks'] = api.list(playlist['tracks']['href'], {'limit': 100})
    data = []
    for playlist in playlists:
        data.append(
            {
                "name": playlist["name"],
                "tracks": [{
                    "name": track["track"]["name"],
                    "uri": track["track"]["uri"],
                    "artists": ', '.join([artist['name'] for artist in track['track']['artists']]),
                    "album": track['track']["album"]["name"]
                } for track in playlist['tracks']]
            }
        )
    with open('backup.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
    log("Done!")
