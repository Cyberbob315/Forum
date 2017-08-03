from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from . import models
from threads import permissions as comment_permissions


class DeleteCommentAPIView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        comment_permissions.DeleteOwnThreadComment
    )

    def delete(self, request, pk):
        comment = get_object_or_404(models.Comment, pk=pk)
        comment.delete()
        data = {
            'success': True
        }
        return Response(data, status=status.HTTP_200_OK)
