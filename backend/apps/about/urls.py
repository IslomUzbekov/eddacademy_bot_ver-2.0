from rest_framework.routers import DefaultRouter

from .views import AboutViewSet, InstitutionReviewViewSet

router = DefaultRouter()
router.register(r"about", AboutViewSet, basename="about")
router.register(
    r"institution_review", InstitutionReviewViewSet, basename="institution review"
)

urlpatterns = router.urls
