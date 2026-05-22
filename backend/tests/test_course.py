from apps.courses.models import Category, Course
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CourseReviewApiTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Cat", slug="test-cat")
        self.course = Course.objects.create(
            title="Test Course",
            category=self.category,
            description="desc",
            includes_courses=1,
            level="Boshlang'ich",
            duration=1,
            price=100000,
            discount_price=0,
        )
        self.url = "/api/course_review/"

    def test_create_course_review_success(self):
        payload = {
            "course": self.course.id,
            "user_id": "12345",
            "score": 5,
            "comment": "Zo'r kurs",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_review_invalid_score(self):
        payload = {
            "course": self.course.id,
            "user_id": "12345",
            "score": 10,  # invalid
            "comment": "bad score",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
