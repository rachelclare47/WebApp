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

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/ToP/'


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^ToP/', include('ToP.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/password/reset/$', views.password_reset, {'template_name': 'registration/password_reset_form.html'}),
    url(r'^accounts/password/reset_complete/$', views.password_reset_complete, name = 'password_reset_complete'),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
