"""
Automated Quality Control & Unit Tests for AI Business Solutions Flask App
Verifies all routes, API endpoints, chatbot responses, and contact form handling.
"""

import unittest
import json
import os
from app import app, MESSAGES_FILE, find_ai_response

class TestAIBusinessSolutions(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_homepage_loads(self):
        """Verify the homepage renders with 200 OK and contains all key sections."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        
        # Check required business branding
        self.assertIn("AI Business Solutions", content)
        self.assertIn("Websites, AI Automation & Digital Solutions", content)
        
        # Check required sections
        self.assertIn("Business Website Development", content)
        self.assertIn("Python Automation", content)
        self.assertIn("AI Chatbot Integration", content)
        self.assertIn("PDF/Document Q&A Systems", content)
        self.assertIn("AI Content Solutions", content)
        
        # Check portfolio items
        self.assertIn("Bella Cucina Bistro", content)
        self.assertIn("Apex Flow Operations", content)
        self.assertIn("DocuQuery AI Assistant", content)
        
        # Check contact form elements
        self.assertIn("contactForm", content)
        self.assertIn("contactName", content)
        self.assertIn("contactPhone", content)
        self.assertIn("contactEmail", content)
        self.assertIn("contactMessage", content)

    def test_ai_assistant_intent_matching(self):
        """Verify that the AI assistant responds correctly without external APIs."""
        # Test greeting
        res_hi = find_ai_response("Hello, what is this?")
        self.assertIn("Welcome", res_hi["reply"])
        self.assertTrue(len(res_hi["suggestions"]) > 0)

        # Test services
        res_serv = find_ai_response("What services do you offer?")
        self.assertIn("Python Automation", res_serv["reply"])

        # Test website cost
        res_price = find_ai_response("How much does a website cost?")
        self.assertIn("$150", res_price["reply"])

        # Test Python automation
        res_py = find_ai_response("How can Python automate my tasks?")
        self.assertIn("Python Automation", res_py["reply"])

        # Test PDF Q&A
        res_pdf = find_ai_response("Can you search through PDF contracts?")
        self.assertIn("PDF/Document Q&A", res_pdf["reply"])

    def test_api_chat_endpoint(self):
        """Verify the POST /api/chat endpoint."""
        response = self.client.post(
            '/api/chat',
            data=json.dumps({"message": "What services do you offer?"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["status"], "success")
        self.assertIn("reply", data)
        self.assertTrue(len(data["suggestions"]) > 0)

    def test_api_contact_submission(self):
        """Verify the POST /api/contact endpoint handles valid and invalid inputs."""
        # Test valid submission
        valid_payload = {
            "name": "Alex Freelance Client",
            "phone": "+92 300 1234567",
            "email": "alex@example.com",
            "service": "Python Automation",
            "message": "We need a Python script to scrape daily pricing from 3 portals."
        }
        res_valid = self.client.post(
            '/api/contact',
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(res_valid.status_code, 200)
        valid_data = json.loads(res_valid.data.decode('utf-8'))
        self.assertEqual(valid_data["status"], "success")

        # Test missing field (missing message and phone)
        res_invalid = self.client.post(
            '/api/contact',
            data=json.dumps({"name": "Incomplete", "email": "inc@example.com"}),
            content_type='application/json'
        )
        self.assertEqual(res_invalid.status_code, 400)

        # Test missing phone
        res_no_phone = self.client.post(
            '/api/contact',
            data=json.dumps({
                "name": "No Phone User",
                "email": "nophone@example.com",
                "message": "Hello without phone"
            }),
            content_type='application/json'
        )
        self.assertEqual(res_no_phone.status_code, 400)

        # Test invalid email
        res_bad_email = self.client.post(
            '/api/contact',
            data=json.dumps({
                "name": "Jane",
                "phone": "+92 300 1234567",
                "email": "not-an-email",
                "message": "Hello"
            }),
            content_type='application/json'
        )
        self.assertEqual(res_bad_email.status_code, 400)

    def test_api_portfolio_endpoint(self):
        """Verify the GET /api/portfolio/<id> returns structured data."""
        res_restaurant = self.client.get('/api/portfolio/restaurant-website')
        self.assertEqual(res_restaurant.status_code, 200)
        data = json.loads(res_restaurant.data.decode('utf-8'))
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["project"]["title"], "Bella Cucina Bistro")

        # Test invalid project ID
        res_404 = self.client.get('/api/portfolio/non-existent-project')
        self.assertEqual(res_404.status_code, 404)

if __name__ == '__main__':
    unittest.main()
