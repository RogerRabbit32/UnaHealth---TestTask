from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GlucoseLevelViewSet

router = DefaultRouter()
router.register(r'levels', GlucoseLevelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
