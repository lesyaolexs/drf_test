from rest_framework.routers import DefaultRouter

from app.views import GroupViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"groups", GroupViewSet, basename="groups")
urlpatterns = router.urls
