"""WAD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from ToP import views
from registration.backends.simple.views import RegistrationView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import password_reset


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/ToP/'


urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/password_change/$', auth_views.password_change, name='password_change'),
    url(r'^accounts/password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^accounts/password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^ToP/', include('ToP.urls')),
    url(r'^admin/', admin.site.urls),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
