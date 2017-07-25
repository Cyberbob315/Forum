from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken




class LoginViewSet(viewsets.ViewSet):
    """Check email and password and return an auth token"""
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""
        return Response({'username':request.user.name})
