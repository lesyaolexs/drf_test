from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

from app.views import CleanDBView, GroupViewSet, UserViewSet
from drf_test import settings

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"groups", GroupViewSet, basename="groups")

urlpatterns = [
    path("cleanup/", CleanDBView.as_view()),
]
urlpatterns += router.urls + static(settings.STATIC_URL)
