from django.conf.urls import url
from ToP import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^top-rated/$', views.top_rated, name='top_rated'),
    url(r'^most_viewed/$', views.most_viewed, name='most_viewed'),
    url(r'^playlist/(?P<playlist_name_slug>[\w\-]+)/$', views.show_playlist, name='show_playlist'),
    url(r'playlist/(?P<playlist_name_slug>[\w\-]+)/add_song/$', views.add_song, name='add_song'),
    url(r'^create_playlist/$', views.create_playlist, name='create_playlist'),
    url(r'^my_playlists/$', views.my_playlists, name='my_playlists'),
    url(r'^home/accounts/password_change/$', auth_views.password_change, name='password_change'),
    url(r'^accounts/password_change/$', auth_views.password_change, name='password_change'),
    url(r'^accounts/password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^view_all_playlists/$', views.view_all_playlists, name='view_all_playlists'),
    url(r'playlist/(?P<playlist_name_slug>[\w\-]+)/comment/$', views.add_comment_to_playlist, name='add_comment'),
    url(r'playlist/(?P<playlist_name_slug>[\w\-]+)/rating/$', views.add_rating, name='add_rating'),
]

