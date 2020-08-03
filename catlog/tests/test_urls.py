from django.test import SimpleTestCase
from django.urls import resolve, reverse

from catlog.views import search, detail


class TestUrls(SimpleTestCase):

    def test_search_url_is_resolved(self):
        # Issue a GET request.
        response = self.client.get('/catalogue/search/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    # Checking URL search is resolved
    def test_search_url_is_resolved(self):
        url = reverse('catlog:search')
        self.assertEquals(resolve(url).func, search)

    # Checking URL search is resolved
    def test_detail_url_is_resolved(self):
        url = reverse('catlog:detail')
        self.assertEquals(resolve(url).func, detail)
