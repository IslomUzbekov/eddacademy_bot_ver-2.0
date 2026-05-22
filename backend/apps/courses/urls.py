from rest_framework.routers import DefaultRouter

from .views import CourseReviewViewSet, CourseViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"course_review", CourseReviewViewSet, basename="course review")

urlpatterns = router.urls
