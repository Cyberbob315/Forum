from rest_framework import permissions
from rest_framework import viewsets

from comments.models import Comment
from threads.api.permissions import DeleteOwnThreadComment
from threads.api.pagination import UserThreadCommentPagination
from .serializers import CommentSerializer, CommentEditDeleteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = UserThreadCommentPagination

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Comment.objects.get(pk=pk)

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializer
        return CommentEditDeleteSerializer

    def get_permissions(self):
        if self.action in ('update', 'destroy'):
            self.permission_classes = (permissions.IsAuthenticated,
                                       DeleteOwnThreadComment,)
        return super().get_permissions()

    def get_queryset(self):
        student_id = self.request.GET.get('student_id', '')
        queryset = Comment.objects.filter(author__student_id=student_id)
        return queryset
