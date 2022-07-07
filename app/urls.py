from rest_framework.routers import DefaultRouter

from app.views import CustomGroupViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"groups", CustomGroupViewSet, basename="groups")
urlpatterns = router.urls
