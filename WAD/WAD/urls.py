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


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/ToP/'


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^ToP/', include('ToP.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/password/change/$', password_change, {
        'template_name': 'registration/password_change_form.html'},
        name="password_change"),
    url(r'^accounts/password/change/done/$', password_change_done, {
        'template_name': 'registration/password_change_done.html'},
        name="password_change_done"),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    ]