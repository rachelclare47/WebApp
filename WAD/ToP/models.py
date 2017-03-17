from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Playlist(models.Model):
    
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='playlist_images',blank=True)
    author = models.URLField(max_length=128, unique=False)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Playlist, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Song(models.Model):
    playlists = models.ForeignKey(Playlist)
    title = models.CharField(max_length=128, unique=False)
    artist = models.CharField(max_length=128, unique=False)
    genre = models.CharField(max_length=128, unique=False)
    
    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title
    
class UserProfile(models.Model):
    # Links UserProfile to a User model instance
    user = models.OneToOneField(User)
    
    # Additional attributes
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username
    def __unicode__(self):
        return self.user.username
