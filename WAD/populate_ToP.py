import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD.settings')
import django
django.setup()
from ToP.models import Playlist, Song

def populate():
	# Lists of dictionaries containing the Songs we want to add
	# into each playlist.
	# Then create a dictionary of dictionaries for the playlists.
	# This allows us to iterate through each data structure and add data
	
	chill_songs = [
		{"title": "Little Talks",
		 "artist": "Of Monsters and Men",
		 "genre": "Indie"},
		{"title": "Tru",
		 "artist": "Lloyd",
		 "genre": "R&B/Soul"} ]
	
	hiphop_songs = [
		{"title": "Rap God",
		 "artist": "Eminem",
		 "genre": "Hip Hop"},
		{"title": "Still D.R.E",
		 "artist": "Dr Dre ft. Snoop Dogg",
		 "genre": "Hip Hop"} ]
	
	kpop_songs = [
		{"title": "Spy",
		 "artist": "Super Junior",
		 "genre": "K-Pop"},
		{"title": "I NEED U",
		 "artist": "BTS",
		 "genre": "K-Pop"} ]
	
	playlists = {"Chill": {"songs": chill_songs},
				 "Hip Hop": {"songs": hiphop_songs},
				 "K-Pop": {"songs": kpop_songs} }
	
	# Code below goes through playlists dictionary, then adds each playlist
	# and adds all associated songs to that playlist
	
	for pl, playlist_data in playlists.items():
		p = add_playlist(pl)
		for song in playlist_data["songs"]:
			add_song(p, song["title"], song["artist"], song["genre"])
	
	# Print out the playlists we have added
	
	for p in Playlist.objects.all():
		for song in Song.objects.filter(playlists=p):
			print("- {0} - {1}".format(str(p), str(song)))
			
def add_song(p, title, artist, genre):
	song = Song.objects.get_or_create(playlists=p, title=title)[0]
	song.artist=artist
	song.genre=genre
	song.save()
	return song

def add_playlist(name):
	p = Playlist.objects.get_or_create(name=name)[0]
	p.save()
	return p

# Start execution here
if __name__ == '__main__':
	print("Starting ToP population script...")
	populate()