from django.db import models


class Application(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    student_name = models.CharField(max_length=255, blank=True) # если заявка на другого человека
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course.title if self.course else 'Не указано'}"
