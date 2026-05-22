from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="category")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="slug")
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ("Boshlang'ich", "Boshlang'ich"),
        ("O'rtacha", "O'rtacha"),
        ("Murakkab", "Murakkab"),
    ]

    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField()
    includes_courses = models.PositiveSmallIntegerField(default=1, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="Boshlang'ich")
    duration = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    discount_price = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    has_certificate = models.BooleanField(
        default=False, blank=True, verbose_name="Has certificate"
    )
    is_free = models.BooleanField(default=False, verbose_name="🟩 Free course")
    is_career_path = models.BooleanField(default=False, verbose_name="🟦 Career path")
    is_skill_path = models.BooleanField(default=False, verbose_name="🟪 Skill path")
    is_cert_path = models.BooleanField(
        default=False, verbose_name="🟨 Certification path"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.title


class Rating(models.Model):
    course = models.ForeignKey(Course, related_name="ratings", on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    score = models.FloatField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reyting"
        verbose_name_plural = "Reytinglar"

    def __str__(self):
        return f"{self.course.title} | {self.score} by {self.user_id}"


class CourseReview(models.Model):
    course = models.ForeignKey(
        Course, related_name="course_review", on_delete=models.CASCADE
    )
    user_id = models.CharField(max_length=100)
    score = models.FloatField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
