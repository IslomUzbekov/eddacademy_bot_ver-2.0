from django.db.models import Avg
from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_rating(self, obj):
        avg = obj.ratings.aggregate(avg=Avg("score"))["avg"]
        return round(avg, 1) if avg is not None else 0.0
