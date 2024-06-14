# Overview
This repository contain a python program which duplicates your Spotify playlists to Youtube.

# Requirements
- Python 3.x
- Installed the required dependecies listed in `requirements.txt`
- Setting up credentials:
1. Configure [Spotify web API](https://developer.spotify.com/documentation/web-api) credentials.
2. Get your **client ID**, **client secret**, and **redirect URI** that can be obtained through the [dashboard](https://developer.spotify.com/dashboard).
3. Pass those values into a .env file with this template:\
SPOTIPY_CLIENT_ID = ' '\
SPOTIPY_CLIENT_SECRET = ' '\
SPOTIPY_REDIRECT_URI = ' '
4. Configure Youtube API credentials by running `ytmusicapi oauth`. This will create a file `oauth.json` in the current directory.