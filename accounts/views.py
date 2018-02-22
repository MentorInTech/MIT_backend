import json
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
import requests

from .serializers import ProfileSerializer


class UserActivationView(APIView):
    """

    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + reverse('user-activate')
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        content = result.json()
        return Response(content)


class Profile(APIView):
    """API resource for user profile.

    get:
    Get user profile.

    put:
    Update user profile.
    """

    def get(self, request: Request) -> Response:
        user = request.user
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        user = request.user
        serializer = ProfileSerializer(user.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
