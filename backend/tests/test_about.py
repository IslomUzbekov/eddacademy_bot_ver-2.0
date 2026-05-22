from rest_framework import status
from rest_framework.test import APITestCase


class InstitutionReviewApiTests(APITestCase):
    def test_create_institution_review_success(self):
        payload = {
            "user_id": "12345",
            "review": "Ajoyib markaz",
        }
        response = self.client.post("/api/institution_review/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
