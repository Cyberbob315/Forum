from enum import Enum
from django.db.models import Q
from django.db.models.aggregates import Count
from django.utils.text import slugify
from rest_framework import generics
from .serializers import ThreadModelSerializer
from .pagination import StandardResultsPagination
from threads.models import Thread

SUBFORUM_ALL_SELECT = 'All'
FILTER_SELECT_NONE = 'None'


class SearchFilter(Enum):
    view_increase = 'Total views ascending'
    view_decrease = 'Total views descending'
    like_increase = 'Total likes ascending'
    like_decrease = 'Total likes descending'


class ThreadSearchView(generics.ListAPIView):
    serializer_class = ThreadModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        subforum_key = self.request.GET.get('subforum', SUBFORUM_ALL_SELECT)
        filter_key = self.request.GET.get('filter', FILTER_SELECT_NONE)
        queryset = Thread.objects.filter(
            Q(content__icontains=query) |
            Q(title__icontains=query)
        )
        if subforum_key != SUBFORUM_ALL_SELECT:
            subforum_key = slugify(subforum_key)
            queryset = queryset.filter(subforum__slug__iexact=subforum_key)
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
