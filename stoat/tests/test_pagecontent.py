from base_test import StoatTestCase, get

from stoat.models import Page, PageContent


class PageContentTestCase(StoatTestCase):
    def test_pagecontent_creation(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        pc1 = PageContent.objects.get(page=p, title='Body')
        pc2 = PageContent.objects.get(page=p, title='Sidebar Heading')
        pc3 = PageContent.objects.get(page=p, title='Sidebar Body')

        self.assertEqual(pc1.content, '')
        self.assertEqual(pc2.content, '')
        self.assertEqual(pc3.content, '')

    def test_pagecontent_deletion(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        pc1 = get(PageContent, page=p, title='Body')
        pc2 = get(PageContent, page=p, title='Sidebar Heading')
        pc3 = get(PageContent, page=p, title='Sidebar Body')
        pc4 = get(PageContent, page=p, title='Test Int')

        self.assertEqual(pc1.content, '')
        self.assertEqual(pc2.content, '')
        self.assertEqual(pc3.content, '')
        self.assertEqual(pc4, None)

        p.template = 'Other'
        p.save()

        pc1 = get(PageContent, page=p, title='Body')
        pc2 = get(PageContent, page=p, title='Sidebar Heading')
        pc3 = get(PageContent, page=p, title='Sidebar Body')
        pc4 = get(PageContent, page=p, title='Test Int')

        self.assertEqual(pc1.content, '')
        self.assertEqual(pc2, None)
        self.assertEqual(pc3, None)
        self.assertEqual(pc4.content, '')

    def test_pagecontent_preservation(self):
        p = Page.add_root(title='Sample', slug='sample', template='Default')
        p.save()

        pc1 = get(PageContent, page=p, title='Body')
        pc1.content = 'Testing Content'
        pc1.save()

        pc1 = get(PageContent, page=p, title='Body')
        self.assertEqual(pc1.content, 'Testing Content')

        p.template = 'Other'
        p.save()

        pc1 = get(PageContent, page=p, title='Body')
        self.assertEqual(pc1.content, 'Testing Content')
