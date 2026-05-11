from django.db import models


class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    published_at = models.DateTimeField()
    image_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title
