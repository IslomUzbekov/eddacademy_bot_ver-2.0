import logging

from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Course, CourseReview
from .serializers import CourseReviewSerializer, CourseSerializer

logger = logging.getLogger(__name__)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseReviewViewSet(viewsets.ModelViewSet):
    queryset = CourseReview.objects.all().order_by("-created_at")
    serializer_class = CourseReviewSerializer

    def create(self, request, *args, **kwargs):
        logger.debug("CourseReview payload: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("CourseReview validation errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        logger.info("CourseReview created id=%s", serializer.instance.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
