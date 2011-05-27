from base_test import StoatTestCase

from stoat.models import Page

class PageViewsTestCase(StoatTestCase):
    def test_slug(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        resp = self.client.get('/sample/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('page' in resp.context)

        self.assertTrue("Sample" in resp.content)

    def test_noslug(self):
        p = Page.add_root(title='Main', slug='', template='Default')
        p.save()

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('page' in resp.context)

        self.assertTrue("Main" in resp.content)

    def test_child(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        p2 = p.add_child(title='Cats', slug='cats', template='Default')
        p2.save()

        resp = self.client.get('/sample/cats/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('page' in resp.context)

        self.assertTrue("Cats" in resp.content)

    def test_404(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        resp = self.client.get('/nom/')
        self.assertEqual(resp.status_code, 404)


    def test_trailing_slash_redirect(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        resp = self.client.get('/sample')

        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'], 'http://testserver/sample/')

    def test_trailing_slash_404(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        resp = self.client.get('/nom')

        self.assertEqual(resp.status_code, 404)

