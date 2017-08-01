from django.utils.text import slugify
from rest_framework import generics
from .serializers import ThreadModelSerializer
from .pagination import StandardResultsPagination
from threads.models import Thread

SUBFORUM_ALL_SELECT = 'All'


class ThreadSearchView(generics.ListAPIView):
    serializer_class = ThreadModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        subforum_key = self.request.GET.get('subforum',SUBFORUM_ALL_SELECT)
        queryset = Thread.objects.filter(content__icontains=query)
        if subforum_key != SUBFORUM_ALL_SELECT:
            subforum_key = slugify(subforum_key)
            queryset = queryset.filter(subforum__slug__iexact=subforum_key)
        return queryset
