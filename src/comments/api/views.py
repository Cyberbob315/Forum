from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from threads.api import permissions as comment_permissions
from threads.api.pagination import UserThreadCommentPagination
from .serializers import CommentSerializer


class UserCommentAPIView(ListAPIView):
    pagination_class = UserThreadCommentPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        student_id = self.request.GET.get('student_id','')
        queryset = Comment.objects.filter(author__student_id=student_id)
        return queryset

class DeleteCommentAPIView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        comment_permissions.DeleteOwnThreadComment
    )

    def delete(self, request, pk):
        print('delete')
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        data = {
            'success': True
        }
        return Response(data, status=status.HTTP_200_OK)

