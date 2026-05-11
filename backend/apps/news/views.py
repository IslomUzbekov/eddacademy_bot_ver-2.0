from rest_framework import viewsets

from .models import NewsPost
from .serializers import NewsPostSerializer


class NewsPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsPost.objects.all()
    serializer_class = NewsPostSerializer
