from django.conf.urls import url
from ToP import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^top-rated/$', views.top_rated, name='top_rated'),
    url(r'^most-listened/$', views.most_listened, name='most_listened'),
    url(r'^playlist/(?P<playlist_name_slug>[\w\-]+)/$', views.show_playlist, name='show_playlist'),
    url(r'^create_playlists/$', views.create_playlists, name='create_playlists'),
    url(r'^my_playlists/$', views.my_playlists, name='my_playlists'),
    url(r'^view_all_playlists/$', views.view_all_playlists, name='view_all_playlists'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
]

