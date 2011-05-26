from base_test import StoatTestCase

from stoat.models import Page, PageContent

class PageTemplatesTestCase(StoatTestCase):
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
