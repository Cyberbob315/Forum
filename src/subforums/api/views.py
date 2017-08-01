from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from subforums.models import Subforum


class SubforumListAPIView(generics.ListAPIView):
    serializer_class = serializers.SubforumModelSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        return Subforum.objects.all()
