from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import MessageViewSet


router = DefaultRouter()
router.register(r'message', MessageViewSet, basename='messages')

urlpatterns = [path("", include(router.urls))]
