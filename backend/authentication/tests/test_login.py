from django.test import TestCase
from rest_framework.test import APIClient


class LoginAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_endpoint_exists(self):
        """
        Verify login endpoint responds.
        """

        response = self.client.post(
            "/api/v1/auth/login/",
            {},
            format="json",
        )

        self.assertNotEqual(
            response.status_code,
            404,
        )