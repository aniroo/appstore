from django.test import TestCase
import json
import logging

logger = logging.getLogger (__name__)

# Create your tests here.

class AppTests(TestCase):

    """
    Test urls, views, and interfaces to application management infrastructure.
    """

    def log_context(self, response):
        logger.info (f"-- response.context: {response.context}")
        
    def test_app_list(self):
        logger.info (f"-- testing app list")
        response = self.client.get('/apps/')
        self.assertEqual(response.status_code, 200)
        self.log_context (response)
        
    def test_app_start(self):
        logger.info (f"-- testing app start")
        response = self.client.get('/start?app_id=x')
        self.assertEqual(response.status_code, 301)
        self.log_context (response)

    def test_app_delete(self):
        logger.info (f"-- testing app delete")
        response = self.client.post("/list_pods/", {
            "sid" : "xyz"
        })
        self.assertEqual(response.status_code, 302)
        self.log_context (response)
