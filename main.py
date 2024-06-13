import os
import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials # to fetch unrelated data of a user
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

# setting up the credentials
load_dotenv()

class SpotifyToYoutube:
    def __init__(self,oauth_json: str):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-read-private'))
        self.oauth_json = oauth_json
        self.yt = YTMusic(oauth_json)

    def get_spo_playlists(self) -> list:
        """
        Fetch saved playlists by the user

        Returns:
            An array of tuples containing playlist id, playlist name, and playlist owner.
        """
        results = self.sp.current_user_playlists()
        
        ids = [item['id'] for item in results['items']]
        names = [item['name'] for item in results['items']]
        owners = [item['owner']['display_name'] for item in results['items']]
        
        playlist_ids = list(zip(ids,names,owners))
        return playlist_ids

    def get_spo_songs(self,playlist_id: str) -> list:
        """
        Fetch songs that contain in a playlist
        
        Args:
            playlist_id: a Spotify playlist ID

        Returns:
            an array of the artist name and song title
        """

        results = self.sp.playlist_items(playlist_id=playlist_id)

        song_list = []
        for i in range(len(results['items'])):
            song_name = results['items'][i]['track']['name']
            song_artist = results['items'][i]['track']['artists'][0]['name']
            song_list.append(song_artist+' '+song_name)
        return song_list

    def from_spo_to_yt(self) -> None:
        """
        Move Spotify playlists to Youtube
        
        Args:
            oauth_json: name of a json file that contain Youtube API credentials
        """
        yt_playlists = self.yt.get_library_playlists()
        yt_playlist_names = set([yt_playlists[i]['title'] for i in range(len(yt_playlists))])

        playlists = self.get_spo_playlists()

        for playlistid,name,owner in playlists:
            if name not in yt_playlist_names:
                playlist_yt = self.yt.create_playlist(title=name,description=name+' created by '+owner+' from Spotify')
                songlist = self.get_spo_songs(playlistid)
                for song in songlist:
                    search_results = self.yt.search(song)
                    if search_results:
                        self.yt.add_playlist_items(playlist_yt,[search_results[0]['videoId']])
                        print(f'Succesfully added {song} to {name} playlist')
                        time.sleep(5)
                time.sleep(30)
            else:
                print(f'Playlist {name} is already available in your Youtube account')

if __name__ == "__main__":
    spotify_to_youtube = SpotifyToYoutube('oauth.json')
    spotify_to_youtube.from_spo_to_yt()