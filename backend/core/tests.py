from django.test import TestCase
class HealthEndpointTest(TestCase):
    def test_health(self):
        r=self.client.get('/health/')
        self.assertEqual(r.status_code,200)
