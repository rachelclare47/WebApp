from django.conf.urls import url
from ToP import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]