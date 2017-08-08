from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status

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

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.student_id != self.request.user.student_id:
            self.perform_destroy(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'result': "Can't delete yourself!"},
                        status=status.HTTP_400_BAD_REQUEST)
