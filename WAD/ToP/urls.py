from django.conf.urls import url
from ToP import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^top-rated/$', views.top_rated, name='top_rated'),
    url(r'^most_viewed/$', views.most_viewed, name='most_viewed'),
    url(r'^playlist/(?P<playlist_name_slug>[\w\-]+)/$', views.show_playlist, name='show_playlist'),
    url(r'playlist/(?P<playlist_name_slug>[\w\-]+)/add_song/$', views.add_song, name='add_song'),
    url(r'^create_playlist/$', views.create_playlist, name='create_playlist'),
    url(r'^my_playlists/$', views.my_playlists, name='my_playlists'),
    url(r'^view_all_playlists/$', views.view_all_playlists, name='view_all_playlists'),
    url(r'^password_change/$', views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', views.PasswordChangeDoneView.as_view(), name='password_change_done')
]

