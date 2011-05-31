from base_test import StoatTestCase

class NavigationTestCase(StoatTestCase):
    def test_nav_roots(self):
        resp = self.client.get('/navigator/')
        self.assertEqual(resp.status_code, 200)

