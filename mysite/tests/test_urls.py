# mysite/tests/test_urls.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class URLTests(TestCase):
    def setUp(self):
        # Create test client
        self.client = Client()
        
        # Create superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create normal user
        self.normal_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='userpass123'
        )

    def test_superuser_access(self):
        # Test admin login
        login_success = self.client.login(
            username='admin',
            password='adminpass123'
        )
        self.assertTrue(login_success)
        
        # Test admin page access
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        
        # Test regular login page access
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_normal_user_access(self):
        # Test normal user login
        login_success = self.client.login(
            username='testuser',
            password='userpass123'
        )
        self.assertTrue(login_success)
        
        # Test admin page access (should be restricted)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        
        # Test regular login page access
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_non_existent_user(self): #test login with non-existent user
        login_success = self.client.login(
            username='nonexistent',
            password='wrongpass'
        )
        self.assertFalse(login_success)

        response = self.client.get('/admin/') #test login page access
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get('/accounts/login/') #test login page access
        self.assertEqual(response.status_code, 200)

class SessionSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    # def test_proper_logout_handling(self): #passing test case - demonstrates proper logout handling
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.post('/accounts/logout/')
    #     self.assertEqual(response.status_code, 302) #passsing test case

    # def test_improper_logout_handling(self): #Failing test- demonstrates improper logout handling
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.get('/accounts/logout/')  # Using GET instead of POST
    #     self.assertEqual(response.status_code, 302)  # This will fail
    
    def test_session_expiration(self):
       
        self.client.login(username='testuser', password='testpass123')

        
        response = self.client.get('/protected/')
        self.assertEqual(response.status_code, 200, "Initial protected view access should succeed")

        # Manually expire the session
        session = self.client.session
        session.set_expiry(0)  # Expire at browser close
        session.save()

        # Clear any existing authentication
        from django.contrib.auth import logout
        logout(self.client)

        
        response = self.client.get('/protected/')

    
        self.assertRedirects(response, '/accounts/login/?next=/protected/')
    
    def test_session_expiration_failure(self):
        """Failing test: Session does not expire due to missing expiration logic."""
        # Log in the user
        self.client.login(username='testuser', password='testpass123')

        # Access the protected view to confirm the user is logged in
        response = self.client.get('/protected/')
        self.assertEqual(response.status_code, 200, "Initial protected view access should succeed")

        # Simulate an architecture breaker: Disable session expiration
        session = self.client.session
        session.set_expiry(None)  # Disable expiration entirely
        session.save()

        # Attempt to access the protected view after "expiration"
        response = self.client.get('/protected/')

        # Intentionally fail the test to demonstrate the architectural breaker
        if response.status_code == 200:
            raise AssertionError(
                "Test failed intentionally: Session expiration logic is missing. "
                "This demonstrates the architectural breaker for session expiration."
            )
        else:
            self.assertRedirects(response, '/accounts/login/?next=/protected/')




    


