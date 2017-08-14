from .views import CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', CommentViewSet, base_name='comment')

