from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from . import models
from . import permissions as thread_permissions


class PostLikeToggleApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        thread = get_object_or_404(models.Thread, pk=pk)
        user = self.request.user
        updated = False
        liked = False
        has_liked = thread.likes.filter(
            student_id=request.user.student_id).exists()
        if has_liked:
            liked = False
            thread.likes.remove(user)
        else:
            liked = True
            thread.likes.add(user)
        updated = True
        like_count = thread.likes.count()
        data = {
            'updated': updated,
            'liked': liked,
            'like_count': like_count,
        }
        return Response(data, status=status.HTTP_200_OK)


class CheckLikeApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        thread = get_object_or_404(models.Thread, pk=pk)
        has_liked = thread.likes.filter(
            student_id=request.user.student_id).exists()
        like_count = thread.likes.count()

        data = {
            'is_liked': has_liked,
            'like_count': like_count,
        }

        return Response(data, status=status.HTTP_200_OK)


class DeleteThreadApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        thread_permissions.DeleteOwnThreadComment
    )

    def get(self, request, pk, format=None):
        thread = get_object_or_404(models.Thread, pk=pk)
        thread.delete()
        data = {
            'success': True
        }
        return Response(data, status=status.HTTP_200_OK)


class PublishThreadApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get(self, request, pk, format=None):
        thread = get_object_or_404(models.Thread, pk=pk)
        thread.published_date = timezone.now()
        thread.save()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_200_OK)
