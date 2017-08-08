from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework import filters
from .serializers import StudentProfileSerializer
from accounts.models import StudentProfile


class UserListAPIView(ListAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return StudentProfile.objects.all().order_by('student_id')


class StudentProfileViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('student_id', 'name', 'email', 'private_email',)
    lookup_field = 'student_id'
