from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from . import models


class PostLikeToggleApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        thread = get_object_or_404(models.Thread, pk=pk)
        user = self.request.user
        updated = False
        liked = False
        if not user.is_authenticated():
            return HttpResponse('You dont have permission to do this')
        if thread.likes.filter(
                student_id__iexact=request.user.id).count > 0:
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
            'likeCount': like_count,
        }
        return Response(data)
