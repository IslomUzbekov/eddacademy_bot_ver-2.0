import logging

import requests
from config import settings

logger = logging.getLogger(__name__)


class ApiService:
    BASE_URL = settings.BACKEND_API_URL

    @staticmethod
    def _log_response(tag: str, response: requests.Response):
        if response.status_code not in (200, 201):
            logger.error("%s ERROR %s: %s", tag, response.status_code, response.text)
        else:
            logger.info("%s OK %s", tag, response.status_code)

    @staticmethod
    def get_courses():
        response = requests.get(f"{ApiService.BASE_URL}courses/")
        ApiService._log_response("GET /courses/", response)
        return response.json() if response.status_code == 200 else []

    @staticmethod
    def get_news():
        response = requests.get(f"{ApiService.BASE_URL}news/")
        ApiService._log_response("GET /news/", response)
        return response.json() if response.status_code == 200 else []

    @staticmethod
    def get_faq():
        response = requests.get(f"{ApiService.BASE_URL}faq/")
        ApiService._log_response("GET /faq/", response)
        return response.json() if response.status_code == 200 else []

    @staticmethod
    def get_about():
        response = requests.get(f"{ApiService.BASE_URL}about/")
        ApiService._log_response("GET /about/", response)
        return response.json() if response.status_code == 200 else []

    @staticmethod
    def post_application(data: dict):
        logger.debug("POST /applications/ payload=%s", data)
        response = requests.post(f"{ApiService.BASE_URL}applications/", json=data)
        ApiService._log_response("POST /applications/", response)
        return response.json() if response.status_code in (200, 201) else None

    @staticmethod
    def post_institution_review(data: dict):
        logger.debug("POST /institution_review/ payload=%s", data)
        response = requests.post(f"{ApiService.BASE_URL}institution_review/", json=data)
        ApiService._log_response("POST /institution_review/", response)
        return response.json() if response.status_code in (200, 201) else None

    @staticmethod
    def post_course_review(data: dict):
        logger.debug("POST /course_review/ payload=%s", data)
        response = requests.post(f"{ApiService.BASE_URL}course_review/", json=data)
        ApiService._log_response("POST /course_review/", response)
        return response.json() if response.status_code in (200, 201) else None
