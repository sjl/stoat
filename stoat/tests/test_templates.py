from base_test import StoatTestCase

class TemplatingTestCase(StoatTestCase):
    def test_default_template(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('stoat/tests/default.html' in [t.name for t in resp.templates])

        self.assertTrue("<h1>Home</h1>" in resp.content)
        self.assertTrue("<h2>home sidebar heading content</h2>" in resp.content)
        self.assertTrue("<p>home sidebar body content</p>" in resp.content)
        self.assertTrue("<section>home body content</section>" in resp.content)

    def test_other_template(self):
        resp = self.client.get('/top-one/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('stoat/tests/other.html' in [t.name for t in resp.templates])

        self.assertTrue("<h1>Top One</h1>" in resp.content)
        self.assertTrue("<section>top one body content</section>" in resp.content)
        self.assertTrue("<aside>1</aside>" in resp.content)

    def test_get_absolute_url(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page'].get_absolute_url(), '/')

        resp = self.client.get('/top-one/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page'].get_absolute_url(), '/top-one/')

        resp = self.client.get('/top-one/one-sub/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page'].get_absolute_url(), '/top-one/one-sub/')

    def test_title(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('<title>Home</title>' in resp.content)
        self.assertTrue('<h1>Home</h1>' in resp.content)

