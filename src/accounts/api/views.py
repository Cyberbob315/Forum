from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from .serializers import (StudentProfileSerializer,
                          StudentProfileCreateSerializer)
from accounts.models import StudentProfile

DEFAULT_PASS = 'hust1234'


class UserListAPIView(ListAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return StudentProfile.objects.all().order_by('student_id')


class ResetPasswordToDefault(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request):
        student_id = request.POST.get('student_id')
        try:
            student = StudentProfile.objects.get(student_id=student_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        student.set_password(DEFAULT_PASS)
        student.save()
        return Response(status=status.HTTP_200_OK)


class StudentProfileViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('student_id', 'name', 'email', 'private_email',)
    lookup_field = 'student_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentProfileCreateSerializer
        return StudentProfileSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.student_id != self.request.user.student_id:
            self.perform_destroy(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'result': "Can't delete yourself!"},
                        status=status.HTTP_400_BAD_REQUEST)
