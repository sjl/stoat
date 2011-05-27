from base_test import StoatTestCase, get

from stoat.models import Page, PageContent

class PageTemplatingTestCase(StoatTestCase):
    def test_default_template(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        pc = PageContent.objects.get(page=p, title='Body')
        pc.content = 'Stoat-Body'
        pc.save()

        pc = PageContent.objects.get(page=p, title='Sidebar Heading')
        pc.content = 'Stoat-Sidebar-Heading'
        pc.save()

        pc = PageContent.objects.get(page=p, title='Sidebar Body')
        pc.content = 'Stoat-Sidebar-Body'
        pc.save()

        resp = self.client.get('/sample/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('stoat/tests/default.html' in [t.name for t in resp.templates])
        self.assertTrue('page' in resp.context)

        self.assertTrue("<h1>Sample</h1>" in resp.content)
        self.assertTrue("<h2>Stoat-Sidebar-Heading</h2>" in resp.content)
        self.assertTrue("<p>Stoat-Sidebar-Body</p>" in resp.content)
        self.assertTrue("<section>Stoat-Body</section>" in resp.content)

    def test_other_template(self):
        p = Page.add_root(title='Sample', slug='sample', template='Other')
        p.save()

        pc = PageContent.objects.get(page=p, title='Body')
        pc.content = 'Stoat-Body'
        pc.save()

        pc = PageContent.objects.get(page=p, title='Test Int')
        pc.content = '1'
        pc.save()

        resp = self.client.get('/sample/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('stoat/tests/other.html' in [t.name for t in resp.templates])
        self.assertTrue('page' in resp.context)

        self.assertTrue("<h1>Sample</h1>" in resp.content)
        self.assertTrue("<section>Stoat-Body</section>" in resp.content)
        self.assertTrue("<aside>1</aside>" in resp.content)

    def test_get_absolute_url(self):
        p0 = Page.add_root(title='Root', slug='', template='Default')
        p0.save()

        p1 = Page.add_root(title='One', slug='one', template='Default')
        p1.save()

        p2 = p1.add_child(title='One and a Half', slug='and-a-half', template='Default')
        p2.save()

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page'].get_absolute_url(), '/')

        resp = self.client.get('/one/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page'].get_absolute_url(), '/one/')

        resp = self.client.get('/one/and-a-half/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page'].get_absolute_url(), '/one/and-a-half/')

    def test_title(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        resp = self.client.get('/sample/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('<title>Sample</title>' in resp.content)
        self.assertTrue('<h1>Sample</h1>' in resp.content)

    def test_fields(self):
        p1 = Page.add_root(title='One', slug='one', template='Default')
        p1.save()

        pc = get(PageContent, page=p1, title='Body')
        pc.content = 'One - Body Content'
        pc.save()

        pc = get(PageContent, page=p1, title='Sidebar Heading')
        pc.content = 'One - Sidebar Heading Content'
        pc.save()

        pc = get(PageContent, page=p1, title='Sidebar Body')
        pc.content = 'One - Sidebar Body Content'
        pc.save()


        p2 = Page.add_root(title='Two', slug='two', template='Other')
        p2.save()

        pc = get(PageContent, page=p2, title='Body')
        pc.content = 'Two - Body Content'
        pc.save()

        pc = get(PageContent, page=p2, title='Test Int')
        pc.content = 'Two - Test Int Content'
        pc.save()


        resp = self.client.get('/one/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('<title>One</title>' in resp.content)
        self.assertTrue('<section>One - Body Content</section>' in resp.content)
        self.assertTrue('<h2>One - Sidebar Heading Content</h2>' in resp.content)
        self.assertTrue('<p>One - Sidebar Body Content</p>' in resp.content)


        resp = self.client.get('/two/')
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('<title>Two</title>' in resp.content)
        self.assertTrue('<section>Two - Body Content</section>' in resp.content)
        self.assertTrue('<aside>Two - Test Int Content</aside>' in resp.content)
