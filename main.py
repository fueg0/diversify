#########################################################
#                  ~ ~ ~ Diversify ~ ~ ~                  #
#    A Spotify WebAPI that ranks the diversity of         #
#    your music library and makes recommendations         #
#    for new music if you'd like.                         #
#    Author: Fuego                                        #
#########################################################

import time
import Artist
import spotipy
from spotipy.oauth2 import SpotifyOAuth

keys = open("keys.txt", "r")

client = keys.readline()
client_secret = keys.readline()
scope = 'user-library-read'

visited_uris = set()
visited_related_uris = set()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client[:-1],
    client_secret=client_secret,
    redirect_uri='http://localhost:8888/callback',
    scope=scope))


def artist_related_to_list(artist_related, level):
    artist_list = []
    empty_artist = [Artist.Artist('', '', [''], graph_level=-1)]

    for relation in artist_related['artists'][0:7]:
        relation_name = relation['name']
        relation_uri = relation['uri']
        relation_artist_object = Artist.Artist(relation_name, relation_uri,
                                               empty_artist, graph_level=level)
        artist_list.append(relation_artist_object)

        if relation_uri not in visited_uris or relation_uri not in visited_related_uris:
            visited_related_uris.add(relation_uri)

    return artist_list


# Could be reincorporated back to track_accumulator
def saved_tracks_to_artists(total_tracks):
    fifty_limit = (total_tracks // 50) * 50
    user_artists = track_accumulator(50, 0, fifty_limit)
    print(user_artists)
    return user_artists


def track_accumulator(limit, offset, offset_cap):
    print("\n\nFetching all user tracks - this may take a while depending on the size of your library")
    user_track_artists = {}
    offset_var = offset
    limit_var = limit

    while True:
        current_tracks = sp.current_user_saved_tracks(limit=limit_var, offset=offset_var)

        for item in current_tracks['items']:
            track = item['track']
            artist_uri = track['artists'][0]['uri']

            if artist_uri not in visited_uris:
                visited_uris.add(artist_uri)
                artist_name = track['artists'][0]['name']
                artist_related = artist_related_to_list(sp.artist_related_artists(artist_uri), 1)

                user_track_artists[artist_uri] = Artist.Artist(artist_name, artist_uri, artist_related)
            else:
                pass

        if offset_var % 100 == 0:
            print("We are ", "{:.2%}".format(offset_var / offset_cap), " of the way through your tracks")
            time.sleep(0.55)
        if offset_var % 200 == 100:
            time.sleep(0.09)
            print("We are still sorting through your tracks...\nThanks for waiting!\n\n")
        if offset_var == offset_cap:
            print("\n\n100%!  Track sorting complete!\nThanks for waiting!\n\n")
            return user_track_artists
        else:
            time.sleep(0.06)
            offset_var += limit_var


# main
saved_tracks = sp.current_user_saved_tracks()
users_artists = saved_tracks_to_artists(saved_tracks['total'])

for artist_key in users_artists:
    artist = users_artists[artist_key]

    for related_artist in artist.related:

        if related_artist.uri in users_artists:
            # print(f"{related_artist.name}  related to  {artist.name}  from saved tracks", f"{artist.graph_level}:{related_artist.graph_level}")
            artist.start_relationship(related_artist)
        else:
            # print(f"{related_artist.name}  related to  {artist.name}", f"{artist.graph_level}:{related_artist.graph_level}")
            artist.add_related_neighbor(related_artist)

for artist_key in users_artists:
    artist = users_artists[artist_key]
    name = artist.name

    print("Related to:", name)
    for rel_artist in artist.neighbors:
        print(f"{users_artists[rel_artist].name}, level {users_artists[rel_artist].graph_level}")
    print("\n\n")
