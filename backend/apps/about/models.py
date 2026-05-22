from django.db import models


class About(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    section = models.CharField(
        max_length=100,
        blank=True,
    )
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class InstitutionReview(models.Model):
    user_id = models.CharField(max_length=100)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id
