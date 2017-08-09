from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from . import serializers
from subjects.models import Subject, Mark


class SubjectViewSet(ModelViewSet):
    serializer_class = serializers.SubjectSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Subject.objects.all()
    lookup_field = 'subject_id'


class MarkViewSet(ModelViewSet):
    serializer_class = serializers.MarkSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Mark.objects.all()
