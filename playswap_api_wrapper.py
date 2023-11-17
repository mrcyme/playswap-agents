import requests

API_URL = 'https://playswap-server.azurewebsites.net'
# API_URL = 'http://localhost:5240'

class PlayswapWrapper:
    def __init__(self, token):
        self.token = token

    def create_playlist(self, title, description):
        data = {
            'name': title,
            'description': description
        }
        response = requests.post(f'{API_URL}/Playlist/', headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }, json=data)
        return response.json()

    def get_playlist(self, playlist_id):
        response = requests.get(f'{API_URL}/Playlist/{playlist_id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        return response.json()

    def get_playlists(self):
        response = requests.get(f'{API_URL}/Playlist/', headers={
            'Authorization': f'Bearer {self.token}'
        })
        if response.status_code != 200:
            raise Exception('Network response was not ok ' + response.reason)
        return response.json()

    def update_playlist(self, playlist_id, data):
        response = requests.put(f'{API_URL}/Playlist/{playlist_id}', headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }, json=data)
        return response.json()

    def delete_playlist(self, playlist_id):
        response = requests.delete(f'{API_URL}/Playlist/{playlist_id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        return response.json()

    def get_influences(self, playlist_id):
        response = requests.get(f'{API_URL}/Playlist/{playlist_id}/Influence', headers={
            'Authorization': f'Bearer {self.token}'
        })
        return response.json()

    def create_influence(self, playlist_id, influence_id):
        response = requests.post(f'{API_URL}/Playlist/{playlist_id}/Influence', headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }, json={"uri": influence_id})
        return response.json()

    def delete_influences(self, playlist_id):
        response = requests.delete(f'{API_URL}/Playlist/{playlist_id}/Influence', headers={
            'Authorization': f'Bearer {self.token}'
        })
        return response.json()

    def get_priority_tracks(self, playlist_id):
        response = requests.get(f'{API_URL}/Playlist/{playlist_id}/Track', headers={
            'Authorization': f'Bearer {self.token}'
        })
        return response.json()

    def create_priority_track(self, playlist_id, track_id):
        response = requests.post(f'{API_URL}/Playlist/{playlist_id}/Track?spotifyTrackUri={track_id}', headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        })
        return response.json()

# Example usage
# api_wrapper = ApiWrapper()
# api_wrapper.set_token('your_token_here')
# playlist_data = {'name': 'New Playlist', ...}
# response = api_wrapper.create_playlist(playlist_data)
# print(response)
