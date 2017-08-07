from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions, generics
from rest_framework import filters
from rest_framework import authentication
from .serializers import AuthTokenSerializer, StudentProfileSerializer
from accounts.models import StudentProfile


class LoginViewSet(viewsets.ViewSet):
    """Check email and password and return an auth token"""
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""
        return Response({'username': request.user.name})


class UserListAPIView(ListAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAdminUser, ]

    def get_queryset(self):
        return StudentProfile.objects.all().order_by('student_id')


class StudentProfileViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('student_id', 'name', 'email', 'private_email',)
    lookup_field = 'student_id'



# class UserDetailAPIView(APIView):
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAdminUser,)
#
#     def get(self, request, student_id, format=None):
#         student = get_object_or_404()
