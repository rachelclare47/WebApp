from django.conf.urls import url
from ToP import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^top-rated/$', views.top_rated, name='top_rated'),
    url(r'^most-listened/$', views.most_listened, name='most_listened'),
    url(r'^playlist/$', views.show_playlist, name='show_playlist'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
]