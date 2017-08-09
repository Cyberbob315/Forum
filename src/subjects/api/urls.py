from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, MarkViewSet

router = DefaultRouter()
router.register('subject', SubjectViewSet)
router.register('mark', MarkViewSet)
