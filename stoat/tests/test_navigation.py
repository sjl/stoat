from base_test import StoatTestCase, get
from stoat.models import Page

class NavigationTestCase(StoatTestCase):
    def test_nav_roots(self):
        resp = self.client.get('/navigator/')
        self.assertEqual(resp.status_code, 200)

        content = resp.content.split('SPLIT')[0]

        self.assertTrue('<li class="roots-root">Home</li>' in content)
        self.assertTrue('<li class="roots-root">Top One</li>' in content)
        self.assertTrue('<li class="roots-root">Top Two</li>' in content)

    def test_nav_roots_and_children(self):
        resp = self.client.get('/navigator/')
        self.assertEqual(resp.status_code, 200)

        content = resp.content.split('SPLIT')[1]

        self.assertTrue('<span class="rac-root">Home</span>' in content)
        self.assertTrue('<span class="rac-root">Top One</span>' in content)
        self.assertTrue('<span class="rac-root">Top Two</span>' in content)

        self.assertTrue('<li class="rac-child">One Sub</li>' in content)

        self.assertTrue('One Sub Sub' not in content)

    def test_nav_siblings(self):
        page = get(Page, url='/')
        real_sibs = set(['/', '/top-one/', '/top-two/'])
        test_sibs = set([p.url for p in page.nav_siblings()])
        self.assertTrue(real_sibs == test_sibs)

        page = get(Page, url='/top-one/')
        test_sibs = set([p.url for p in page.nav_siblings()])
        self.assertTrue(real_sibs == test_sibs)

        page = get(Page, url='/top-one/one-sub/')
        real_sibs = set(['/top-one/one-sub/'])
        test_sibs = set([p.url for p in page.nav_siblings()])
        self.assertTrue(real_sibs == test_sibs)
        
    def test_nav_next_sibling(self):
        page = get(Page, url='/')
        real_sibs = set(['/', '/top-one/', '/top-two/'])
        real_next_sib = '/top-one/'
        self.assertTrue(real_next_sib == page.nav_next_sibling().url)
        
        page = get(Page, url='/top-two/')
        real_next_sib = None
        self.assertTrue(real_next_sib == page.nav_next_sibling())
        
    def test_nav_prev_sibling(self):
        page = get(Page, url='/')
        real_sibs = set(['/', '/top-one/', '/top-two/'])
        real_prev_sib = None
        self.assertTrue(real_prev_sib == page.nav_prev_sibling())
        
        page = get(Page, url='/top-two/')
        real_sibs = set(['/', '/top-one/', '/top-two/'])
        real_prev_sib = '/top-one/'
        self.assertTrue(real_prev_sib == page.nav_prev_sibling().url)

    def test_nav_children(self):
        page = get(Page, url='/')
        real_kids = set([])
        test_kids = set([p.url for p in page.nav_children()])
        self.assertTrue(real_kids == test_kids)

        page = get(Page, url='/top-one/')
        real_kids = set(['/top-one/one-sub/'])
        test_kids = set([p.url for p in page.nav_children()])
        self.assertTrue(real_kids == test_kids)

        page = get(Page, url='/top-one/one-sub/')
        real_kids = set(['/top-one/one-sub/one-sub-sub/'])
        test_kids = set([p.url for p in page.nav_children()])
        self.assertTrue(real_kids == test_kids)
        
    def test_nav_siblings_and_children(self):
        def test_siblings(saclist, urllist):
            urls = set([sib.url for sib, children in saclist])
            return urls == set(urllist)

        def test_children(saclist, urlmap):
            test_urlmap = {}
            for sib, children in saclist:
                test_urlmap[sib.url] = [c.url for c in children]

            return test_urlmap == urlmap


        page = get(Page, url='/')
        real_sibs = ['/', '/top-one/', '/top-two/']
        real_map = {
            '/': [],
            '/top-one/': ['/top-one/one-sub/'],
            '/top-two/': [],
        }
        saclist = page.nav_siblings_and_children()
        self.assertTrue(test_siblings(saclist, real_sibs))
        self.assertTrue(test_children(saclist, real_map))

        page = get(Page, url='/top-one/')
        saclist = page.nav_siblings_and_children()
        self.assertTrue(test_siblings(saclist, real_sibs))
        self.assertTrue(test_children(saclist, real_map))

        page = get(Page, url='/top-one/one-sub/')
        real_sibs = ['/top-one/one-sub/']
        real_map = {
            '/top-one/one-sub/': ['/top-one/one-sub/one-sub-sub/'],
        }
        saclist = page.nav_siblings_and_children()
        self.assertTrue(test_siblings(saclist, real_sibs))
        self.assertTrue(test_children(saclist, real_map))

    def test_breadcrumbs(self):
        page = get(Page, url='/')
        real_crumbs = ['/']
        self.assertTrue(real_crumbs == [p.url for p in page.breadcrumbs()])

        page = get(Page, url='/top-one/')
        real_crumbs = ['/top-one/']
        self.assertTrue(real_crumbs == [p.url for p in page.breadcrumbs()])

        page = get(Page, url='/top-one/one-sub/')
        real_crumbs = ['/top-one/', '/top-one/one-sub/']
        self.assertTrue(real_crumbs == [p.url for p in page.breadcrumbs()])

        page = get(Page, url='/top-one/one-sub/one-sub-sub/')
        real_crumbs = ['/top-one/', '/top-one/one-sub/', '/top-one/one-sub/one-sub-sub/']
        self.assertTrue(real_crumbs == [p.url for p in page.breadcrumbs()])

        page = get(Page, url='/top-one/one-sub-hidden/')
        real_crumbs = ['/top-one/', '/top-one/one-sub-hidden/']
        self.assertTrue(real_crumbs == [p.url for p in page.breadcrumbs()])
