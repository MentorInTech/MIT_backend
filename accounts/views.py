from django.test.client import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProfileSerializer


class UserActivationView(APIView):
    """API resource for user activation

    get:
    Activate user account
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request: Request, uid: str, token: str) -> Response:
        """Handle GET request.

        :param request: DRF request object
        :param uid: user id in base64 encoding
        :param token: activation token
        :return: 200 OK
        """
        c = Client()
        response: Response = c.post(reverse('user-activate'), {'uid': uid, 'token': token})
        return Response(response.content, response.status_code)


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
