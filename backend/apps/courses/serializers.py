from django.db.models import Avg
from rest_framework import serializers

from .models import Course, CourseReview


class CourseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_rating(self, obj):
        avg = obj.course_review.aggregate(avg=Avg("score"))["avg"]
        return round(avg, 1) if avg is not None else 0.0


class CourseReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseReview
        fields = "__all__"
