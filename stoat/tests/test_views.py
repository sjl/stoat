from base_test import StoatTestCase

class ViewsTestCase(StoatTestCase):
    def test_slug(self):
        resp = self.client.get('/top-one/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue("Top One" in resp.content)

    def test_noslug(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue("Home" in resp.content)

    def test_child(self):
        resp = self.client.get('/top-one/one-sub/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue("One Sub" in resp.content)

    def test_404(self):
        resp = self.client.get('/non-existant/')
        self.assertEqual(resp.status_code, 404)


    def test_trailing_slash_redirect(self):
        resp = self.client.get('/top-one')

        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'], 'http://testserver/top-one/')

    def test_trailing_slash_404(self):
        resp = self.client.get('/non-existant')

        self.assertEqual(resp.status_code, 404)

