import logging

from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import About, InstitutionReview
from .serializers import AboutSerializer, InstitutionReviewSerializer

logger = logging.getLogger(__name__)


class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class InstitutionReviewViewSet(viewsets.ModelViewSet):
    queryset = InstitutionReview.objects.all()
    serializer_class = InstitutionReviewSerializer

    def create(self, request, *args, **kwargs):
        logger.debug("InstitutionReview payload: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("InstitutionReview validation errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        logger.info("InstitutionReview created id=%s", serializer.instance.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
