import requests
from config import settings


class ApiService:
    BASE_URL = settings.BACKEND_API_URL

    @staticmethod
    def get_courses():
        response = requests.get(f"{ApiService.BASE_URL}courses/")
        return response.json() if response.status_code == 200 else []

    @staticmethod
    def get_news():
        response = requests.get(f"{ApiService.BASE_URL}news/")
        return response.json() if response.status_code == 200 else []

    @staticmethod
    def get_faq():
        response = requests.get(f"{ApiService.BASE_URL}faq/")
        return response.json() if response.status_code == 200 else []

    @staticmethod
    def get_about():
        response = requests.get(f"{ApiService.BASE_URL}about/")
        return response.json() if response.status_code == 200 else {}

    @staticmethod
    def post_application(data: dict):
        response = requests.post(f"{ApiService.BASE_URL}applications/", json=data)
        if response.status_code in (200, 201):
            return response.json()
        return None
