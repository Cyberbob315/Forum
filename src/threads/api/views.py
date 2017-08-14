from enum import Enum

from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import authentication, permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from threads.api import permissions as thread_permissions
from threads.models import Thread
from .pagination import StandardResultsPagination, UserThreadCommentPagination
from .serializers import ThreadModelSerializer

SUBFORUM_ALL_SELECT = 'All'


class SearchFilter(Enum):
    none_selected = 'None'
    top_comment = 'Most commented'
    view_increase = 'Total views ascending'
    view_decrease = 'Total views descending'
    like_increase = 'Total likes ascending'
    like_decrease = 'Total likes descending'


class ThreadSearchView(generics.ListAPIView):
    serializer_class = ThreadModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        subforum_key = self.request.GET.get('subforum', SUBFORUM_ALL_SELECT)
        filter_key = self.request.GET.get('filter',
                                          SearchFilter.none_selected.value)
        queryset = Thread.objects.filter(
            Q(content__icontains=query) |
            Q(title__icontains=query)
        ).order_by('-created_date')
        if subforum_key != SUBFORUM_ALL_SELECT:
            subforum_key = slugify(subforum_key)
            queryset = queryset.filter(subforum__slug__iexact=subforum_key)
        if filter_key == SearchFilter.top_comment.value:
            queryset = queryset.annotate(
                total_comment=Count('comments')
            ).order_by('-total_comment')
        if filter_key == SearchFilter.view_decrease.value:
            queryset = queryset.order_by('-view_count')
        if filter_key == SearchFilter.view_increase.value:
            queryset = queryset.order_by('view_count')
        if filter_key == SearchFilter.like_decrease.value:
            queryset = queryset.annotate(total_like=Count('likes')).order_by(
                '-total_like')
        if filter_key == SearchFilter.like_increase.value:
            queryset = queryset.annotate(total_like=Count('likes')).order_by(
                'total_like')
        return queryset


class UserThreadAPIView(generics.ListAPIView):
    serializer_class = ThreadModelSerializer
    pagination_class = UserThreadCommentPagination

    def get_queryset(self):
        student_id = self.request.GET.get('student_id', '')
        queryset = Thread.objects.filter(author__student_id=student_id)
        return queryset


class PostLikeToggleApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk=None):
        thread = get_object_or_404(Thread, pk=pk)
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
        thread = get_object_or_404(Thread, pk=pk)
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

    def delete(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        subforum_slug = thread.subforum.slug
        redirect_link = reverse('forum:detail', kwargs={'slug': subforum_slug})
        thread.delete()
        data = {
            'success': True,
            'redirect_link': redirect_link,
        }
        return Response(data, status=status.HTTP_200_OK)


class PublishThreadApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def put(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        thread.published_date = timezone.now()
        thread.save()
        data = {
            'success': True,
        }
        return Response(data, status=status.HTTP_200_OK)
