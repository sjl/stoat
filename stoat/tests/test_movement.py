from base_test import StoatTestCase, get
from django.contrib.auth.models import User
from stoat.models import Page

class MovementTestCase(StoatTestCase):
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@example.com', 'adminpass')
        user.is_staff = user.is_superuser = True
        user.save()

        return super(MovementTestCase, self).setUp()


    def test_move_inside(self):
        one = get(Page, title='Top One')
        two = get(Page, title='Top Two')

        self.assertTrue(two in one.get_siblings())
        self.assertTrue(two not in one.get_children())

        self.client.login(username='admin', password='adminpass')
        resp = self.client.post('/admin/stoat/page/move-page/', {
            'page': two.id,
            'target': one.id,
            'position': 'inside',
        })
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'], 'http://testserver/admin/stoat/page/')

        one = get(Page, title='Top One')
        two = get(Page, title='Top Two')

        self.assertEqual(two.url, '/top-one/top-two/')
        self.assertTrue(two not in one.get_siblings())
        self.assertTrue(two in one.get_children())

    def test_move_above(self):
        one = get(Page, title='Top One')
        two = get(Page, title='Top Two')
        pages = list(Page.objects.filter(depth=1))

        self.assertTrue(two in pages)
        self.assertTrue(pages.index(one) < pages.index(two))

        self.client.login(username='admin', password='adminpass')
        resp = self.client.post('/admin/stoat/page/move-page/', {
            'page': two.id,
            'target': one.id,
            'position': 'above',
        })
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'], 'http://testserver/admin/stoat/page/')

        one = get(Page, title='Top One')
        two = get(Page, title='Top Two')
        pages = list(Page.objects.filter(depth=1))

        self.assertTrue(two in pages)
        self.assertTrue(pages.index(one) > pages.index(two))

    def test_move_below(self):
        one = get(Page, title='Top Two')
        two = get(Page, title='Top One')
        pages = list(Page.objects.filter(depth=1))

        self.assertTrue(two in pages)
        self.assertTrue(pages.index(one) > pages.index(two))

        self.client.login(username='admin', password='adminpass')
        resp = self.client.post('/admin/stoat/page/move-page/', {
            'page': two.id,
            'target': one.id,
            'position': 'below',
        })
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'], 'http://testserver/admin/stoat/page/')

        one = get(Page, title='Top Two')
        two = get(Page, title='Top One')
        pages = list(Page.objects.filter(depth=1))

        self.assertTrue(two in pages)
        self.assertTrue(pages.index(one) < pages.index(two))

    def test_move_tree(self):
        one = get(Page, title='Top One')
        one_sub = get(Page, title='One Sub')
        one_sub_sub = get(Page, title='One Sub Sub')
        two = get(Page, title='Top Two')

        self.assertTrue(one in two.get_siblings())
        self.assertEqual(one.url, '/top-one/')
        self.assertEqual(one_sub.url, '/top-one/one-sub/')
        self.assertEqual(one_sub_sub.url, '/top-one/one-sub/one-sub-sub/')

        self.client.login(username='admin', password='adminpass')
        resp = self.client.post('/admin/stoat/page/move-page/', {
            'page': one.id,
            'target': two.id,
            'position': 'inside',
        })
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'], 'http://testserver/admin/stoat/page/')

        one = get(Page, title='Top One')
        one_sub = get(Page, title='One Sub')
        one_sub_sub = get(Page, title='One Sub Sub')
        two = get(Page, title='Top Two')

        self.assertTrue(one in two.get_children())
        self.assertEqual(one.url, '/top-two/top-one/')
        self.assertEqual(one_sub.url, '/top-two/top-one/one-sub/')
        self.assertEqual(one_sub_sub.url, '/top-two/top-one/one-sub/one-sub-sub/')


