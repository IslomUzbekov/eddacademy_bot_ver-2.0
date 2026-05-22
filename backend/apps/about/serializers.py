from rest_framework import serializers

from .models import About, InstitutionReview


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"


class InstitutionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionReview
        fields = "__all__"
