from datetime import datetime
import spotipy
from spotipy import oauth2
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import tweepy
import sys
from os import environ

now = datetime.now()
dt_string = now.strftime("%H:%M")

CLIENT_ID = environ['SPO_ID']
CLIENT_SECRET = environ['SPO_SECRET']
scope = "user-read-currently-playing"
username = "kahmeeah"
redirect_uri = "http://localhost:8080"

CONSUMER_KEY = environ['API_KEY']
CONSUMER_SECRET = environ['API_SECRET_KEY']
ACCESS_KEY = environ['ACCESS_TOKEN']
ACCESS_SECRET = environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
tweepy_api = tweepy.API(auth)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET,
                                                           redirect_uri=redirect_uri,
                                                           scope=scope
                                                           ))
current_track = sp.current_user_playing_track()
print(current_track)
        
while True:
    try:
        current_track = sp.current_user_playing_track()
        current_track_id = current_track['item']['id']

        if current_track_id is not None:

            print("Tweeting song...")
            now = datetime.now()
            dt_string = now.strftime("%H:%M")
            tweepy_api.update_status("mimi's spotify " + dt_string + ":" + '\n' + current_track['item']['artists'][0]['name'] + " - " +
                                                            current_track['item']['name'] + '\n' + str(
                                                            current_track['item']['external_urls']['spotify']))
            break
        else:
            continue
    except sp.client.SpotifyException:
        token = util.prompt_for_user_token(username=username,
                                           scope=scope,
                                           client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri=redirect_uri)

        sp = spotipy.Spotify(auth=token)
    except (tweepy.TweepError, TypeError) as e:
        pass

while True:
    try:
        new_track = sp.current_user_playing_track()
        new_track_id = new_track['item']['id']

        if current_track_id is not None and new_track_id != current_track_id:
            
            print("Tweeting song...")
            now = datetime.now()
            dt_string = now.strftime("%H:%M")
            tweepy_api.update_status("mimi's spotify " + dt_string + ":" + '\n' + new_track['item']['artists'][0]['name'] + " - " + 
                                                            new_track['item']['name'] + '\n' + str(
                                                            new_track['item']['external_urls']['spotify']))
            current_track_id = new_track_id
        else:
            continue
    except spotipy.client.SpotifyException:
        token = util.prompt_for_user_token(username=username,
                                           scope=scope,
                                           client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri=redirect_uri)

        sp = spotipy.Spotify(auth=token)
    except (tweepy.TweepError, TypeError)as e:
        pass
