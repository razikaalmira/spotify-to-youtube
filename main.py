import spotipy
from spotipy.oauth2 import SpotifyClientCredentials # to fetch unrelated data of a user
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import os
import time

# setting up the credentials
os.environ['SPOTIPY_CLIENT_ID'] = 'b5734e600d6d431c8a3c78cb170c599c'
os.environ['SPOTIPY_CLIENT_SECRET'] = '14579bc988444acc9f396bce4f9335c8'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8181/callback'


def get_spo_playlists() -> list:
    """
    Fetch saved playlists by the user

    Returns:
        An array of tuples containing playlist id, playlist name, and playlist owner.
    """
    
    scope = "playlist-read-private"
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results2 = sp.current_user_playlists()
    
    ids = [item['id'] for item in results2['items']]
    names = [item['name'] for item in results2['items']]
    owners = [item['owner']['display_name'] for item in results2['items']]
    
    playlist_ids = list(zip(ids,names,owners))
    return playlist_ids

def get_spo_songs(playlist_id: str) -> list:
    """
    Fetch songs that contain in a playlist
    
    Args:
        playlist_id: a Spotify playlist ID

    Returns:
        an array of the artist name and song title
    """
    
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    
    results2 = sp.playlist_items(playlist_id=playlist_id)

    song_list = []
    for i in range(len(results2['items'])):
        song_name = results2['items'][i]['track']['name']
        song_artist = results2['items'][i]['track']['artists'][0]['name']
        song_list.append(song_artist+' '+song_name)
    return song_list

def from_spo_to_yt(oauth_json: str) -> None:
    """
    Move Spotify playlists to Youtube
    
    Args:
        oauth_json: name of a json file that contain Youtube API credentials
    """
    yt = YTMusic(oauth_json)
    yt_playlists = yt.get_library_playlists()
    yt_playlist_names = set([yt_playlists[i]['title'] for i in range(len(yt_playlists))])

    playlists = get_spo_playlists()

    for playlistid,name,owner in playlists:
        if name not in yt_playlist_names:
            playlist_yt = yt.create_playlist(title=name,description=name+' created by '+owner+' from Spotify')
            songlist = get_spo_songs(playlistid)
            for song in songlist:
                search_results = yt.search(song)
                yt.add_playlist_items(playlist_yt,[search_results[0]['videoId']])
                print(f'Succesfully added {song} to {name} playlist')
                time.sleep(30)
        else:
            print(f'Playlist {name} is already available in your Youtube account')

if __name__ == "__main__":
    from_spo_to_yt('oauth.json')