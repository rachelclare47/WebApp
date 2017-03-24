from django.test import TestCase
from ToP.models import *
from ToP.forms import *
from ToP.views import *
from ToP.urls import *
from django.core.urlresolvers import reverse


# Helper method to make a playlist
def add_p(name, views, rating, author):
    p = Playlist.objects.get_or_create(name=name)[0]
    p.views = views
    p.rating = rating
    p.author = author
    p.save()
    return p


# Helper method to make a song
def add_s(title, album, artist, genre):
    s = Song.objects.get_or_create(title=title)[0]
    s.album = album
    s.artist = artist
    s.genre = genre
    s.save()
    return s


# Helper method to make a user
def add_user(username, email, password):
    u = UserProfile.objects.get_or_create(user=username)[0]
    u.email = email
    u.password = password
    u.save()
    return u


class PlaylistMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        # Return true where playlist's views are positive
        playlist = Playlist(name='test', views=-1)
        playlist.save()
        self.assertEqual((playlist.views >= 0), True)

    def test_ensure_slug_is_valid(self):
        # Test that slug creation has lowercase + hyphens
        playlist = Playlist(name='Random Playlist String')
        playlist.save()
        self.assertEqual(playlist.slug, 'random-playlist-string')

    def test_ensure_rating_is_positive(self):
        # Return true where playlist's ratings are positive
        playlist = Playlist(name='test', rating=-1)
        playlist.save()
        self.assertEqual((playlist.rating >= 0), True)

    def test_ensure_rating_is_no_more_than_five(self):
        # Return true where playlist's ratings aren't above 5
        playlist = Playlist(name='test', rating=6)
        playlist.save()
        self.assertEqual((playlist.rating < 6), True)


class HomeViewTests(TestCase):
    def test_home_view_loads_successfully(self):
        # Return a success status code if home page loads
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class TopRatedViewTests(TestCase):
    def test_top_rated_view_without_playlists(self):
        # If no playlists exist, display the appropriate message
        # Also tests that page loads successfully and that context_dict is empty
        response = self.client.get(reverse('top_rated'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no playlists present.")
        self.assertQuerysetEqual(response.context['playlists'], [])

    def test_top_rated_view_with_playlists(self):
        # Make sure that top rated page has playlists displayed
        # Create 4 playlists
        add_p('test', 1, 1, 'wadteam1')
        add_p('temp', 1, 1, 'wadteam1')
        add_p('tmp', 1, 1, 'wadteam1')
        add_p('tmp test temp', 1, 1, 'wadteam1')

        # Check that page loaded and that the response contains the last playlist created
        response = self.client.get(reverse('top_rated'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp test temp')

        # Check that the context has 4 playlists
        num_of_playlists = len(response.context['playlists'])
        self.assertEqual(num_of_playlists, 4)


class ShowPlaylistViewTests(TestCase):
    def test_show_playlist_without_songs(self):
        # If no songs exist in the context, display the appropriate message
        # Also tests that page loads successfully and that context_dict['songs'] is empty
        add_p('test', 1, 1, 'wadteam1')
        response = self.client.get('/ToP/playlist/test/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No songs currently in playlist.")
        self.assertQuerysetEqual(response.context['songs'], [])

    '''def test_show_playlist_with_songs(self):
        # Make sure that individual playlist page has songs displayed
        # Create a playlist to put songs into
        add_p('test', 1, 1)
        # Create 4 songs
        add_s('Tonite', 'Infinite', 'Eminem', 'Rap')
        add_s('Never 2 Far', 'Infinite', 'Eminem', 'Rap')
        add_s('Backstabber', 'Infinite', 'Eminem', 'Rap')
        add_s('Jealousy Woes II', 'Infinite', 'Eminem', 'Rap')

        # Check that page loaded and that the response contains the last song created
        response = self.client.get('/ToP/playlist/test/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jealousy Woes II')

        # Check that the context has 4 songs
        num_of_songs = len(response.context['songs'])
        self.assertEqual(num_of_songs, 4)'''

    def test_show_playlist_view_shows_view_count(self):
        # Make sure that there are views passed through context
        dict = {'visits': 1}
        add_p('test', 1, 1, 'wadteam1')
        response = self.client.get('/ToP/playlist/test/')
        self.assertEqual(response.context['visits'], dict['visits'])

    def test_show_playlist_view_shows_average_rating(self):
        # Make sure that there are ratings passed through context
        add_p('test', 1, 1, 'wadteam1')
        response = self.client.get('/ToP/playlist/test/')
        self.assertContains(response, response.context['total_rating'])


class MostViewedViewTests(TestCase):
    def test_most_viewed_view_without_playlists(self):
        # If no playlists exist, display the appropriate message
        # Also tests that page loads successfully and that context_dict is empty
        response = self.client.get(reverse('most_viewed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no playlists present.")
        self.assertQuerysetEqual(response.context['playlists'], [])

    def test_most_viewed_view_with_playlists(self):
        # Make sure that top rated page has playlists displayed
        # Create 4 playlists
        add_p('test', 1, 1, 'wadteam1')
        add_p('temp', 1, 1, 'wadteam1')
        add_p('tmp', 1, 1, 'wadteam1')
        add_p('tmp test temp', 1, 1, 'wadteam1')

        # Check that page loaded and that the response contains the last playlist created
        response = self.client.get(reverse('most_viewed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp test temp')

        # Check that the context has 4 playlists
        num_of_playlists = len(response.context['playlists'])
        self.assertEqual(num_of_playlists, 4)

'''class AddCommentViewTests(TestCase):
    def test_comment_form_passed_to_template(self):
        # Make sure that a form is passed through the context and page loads
        add_p('test', 1, 1)
        response = self.client.get('/ToP/playlist/test/comment/')
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(response.context['form'], form)'''


class ViewAllPlaylistsTests(TestCase):
    def test_view_all_view_without_playlists(self):
        # If no playlists exist, display the appropriate message
        # Also tests that page loads successfully and that context_dict is empty
        response = self.client.get(reverse('view_all_playlists'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no playlists present.")
        self.assertQuerysetEqual(response.context['playlists'], [])

    def test_view_all_view_with_playlists(self):
        # Make sure that top rated page has playlists displayed
        # Create 4 playlists
        add_p('test', 1, 1, 'wadteam1')
        add_p('temp', 1, 1, 'wadteam1')
        add_p('tmp', 1, 1, 'wadteam1')
        add_p('tmp test temp', 1, 1, 'wadteam1')

        # Check that page loaded and that the response contains the last playlist created
        response = self.client.get(reverse('view_all_playlists'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp test temp')

        # Check that the context has 4 playlists
        num_of_playlists = len(response.context['playlists'])
        self.assertEqual(num_of_playlists, 4)


'''class MyPlaylistsTests(TestCase):
    def test_my_playlists_has_correct_author(self):
        add_p('test', 1, 1, 'wadteam1')
        response = self.client.get(reverse('my_playlists'))
        self.assertEqual(response.status_code, 302)
        for p in response.context['playlists']:
            self.assertEqual(p.author, 'wadteam1')
        num_of_playlists = len(response.context['playlists'])
        self.assertEqual(num_of_playlists, 1)'''

class ToPUrlsTests(TestCase):
    def test_password_change_loads_successfully(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)

    def test_password_change_complete_loads_successfully(self):
        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 302)

    def test_add_song_page_loads_successfully(self):
        add_p('test', 1, 1, 'wadteam1')
        response = self.client.get('/ToP/playlist/test/add_song/')
        self.assertEqual(response.status_code, 302)

    def test_create_playlist_page_loads_successfully(self):
        response = self.client.get(reverse('create_playlist'))
        self.assertEqual(response.status_code, 302)

    def test_my_playlists_page_loads(self):
        response = self.client.get(reverse('my_playlists'))
        self.assertEqual(response.status_code, 302)

    def test_add_comment_page_loads(self):
        add_p('test', 1, 1, 'wadteam1')
        response = self.client.get('/ToP/playlist/test/comment/')
        self.assertEqual(response.status_code, 302)

    def test_add_rating_page_loads(self):
        add_p('test', 1, 1, 'wadteam1')
        response = self.client.get('/ToP/playlist/test/rating/')
        self.assertEqual(response.status_code, 302)
