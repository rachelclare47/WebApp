from __future__ import unicode_literals

from django.db import models

# Create your models here.
"""
class Playlist(models.Model):
    name = models.OneToOneField(Playlist_Name)
    songs = models.OneToOneField(Song_Name)
    views = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='profile_images',blank=True)
    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.OneToOneField(Song_Name)
    artist = models.OneToOneField(Artist_Name)
    album = models.OneToOneField(Album_Name)
    playlists = models.ManyToManyField(Album_Name)
    def __str__(self):
        return self.title
"""
