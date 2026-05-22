from django.contrib import admin

from .models import Category, Course, CourseReview, Rating


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "duration", "price")
    fields = (
        "title",
        "category",
        "description",
        "includes_courses",
        "level",
        "duration",
        "price",
        "discount_price",
        "has_certificate",
        "is_free",
        "is_career_path",
        "is_skill_path",
        "is_cert_path",
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(CourseReview)
