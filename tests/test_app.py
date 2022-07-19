# tests/test_app.py

from http.client import responses
import unittest
import os
import sys
import logging

os.environ['TESTING'] = 'true'

log = logging.getLogger(__name__)

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Home</title>" in html

        assert '<img src="./static/img/lucas/lucas.jpg" class="d-block mx-lg-auto img-fluid rounded-circle" alt="Bootstrap Themes" width="700" height="500" loading="lazy">' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")

        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()

        assert "timeline_posts" in json
        assert len(json['timeline_posts'])  == 0

        # Test POST

        post_data = {
            'name': 'John Doe',
            'email': 'johndoe@mlh.com',
            'content': 'Testing posts with unittest!'
        }

        response = self.client.post("/api/timeline_post", data=post_data)

        # Test /timeline

        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        assert '<h3 class="py-3">Timeline Posts</h3>' in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})

        assert response.status_code == 400
        
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})

        assert response.status_code == 400
        
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": ""})

        assert response.status_code == 400
        
        html = response.get_data(as_text=True)
        assert "Invalid email" in html







