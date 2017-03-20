from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from ToP.models import Playlist, Song, UserProfile,Comment
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PlaylistForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the playlist name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    picture = forms.ImageField(initial=BASE_DIR+" \media\\vinyl-883199_960_720.png")
    ##############################################################
    # FIGURE OUT HOW TO PUT USER URL IN INITIAL HIDDEN FIELD
    author = forms.CharField(widget=forms.HiddenInput(), initial=User )
    ##############################################################
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Playlist
        fields = ('name', 'picture',)

class CommentForm(forms.ModelForm):
   
    class Meta:
        model = Comment
        fields = ('author','text',)

class SongForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the song.")
    artist = forms.CharField(max_length=128, help_text="Please enter the artist of the song.")
    genre = forms.CharField(max_length=128, help_text="Please enter the genre of music.")
    
    class Meta:
        model = Song
        # Hiding the foreign key
        # Can either exclude the playlist field from the form or specify fields to include
        exclude = ('playlists',)
        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label ="Email", max_length=254)

    def save(self, domain_override = None,
             subject_template_name = 'registration/password_reset_subject.txt',
             email_template_name = 'registration/password_reset_email.html',
             use_https = False,
             token_generator = default_token_generator,
             from_email = None,
             request = None,
             html_email_template_name = None):
        """
        Generates a one-use only link for resetting the password and sends to the user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to any user that actually has a
            # password marked as unusable.
            if not user_has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(override)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if user_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject must not contain new lines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)

            if html_email_template_name:
                html_email = laoder.render_to_string(html_email_template_name, c)
            else:
                html_email = None
            send_mail(subject, email, from_email, [user.email], html_message=html_email)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change their password without entering the old password
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    new_password1 = forms.CharField(label="New Password",
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New Password Confirmation",
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code = 'password_mismatch'
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(slef.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


