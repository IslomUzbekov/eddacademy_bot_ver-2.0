from django.db import models


class About(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    section = models.CharField(
        max_length=100,
        blank=True,
    )  # для history, teachers, partners, achievements, reviews и т.д.
    order = models.PositiveIntegerField(default=0)  # для сортировки в админке

    def __str__(self):
        return self.title
