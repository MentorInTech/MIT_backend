from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .serializers import UserSerializer, ProfileSerializer
from .tokens import account_activation_token


class UserCreate(APIView):
    """API to create User.

    post:
    Create new user account.
    """

    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserSerializer

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # TODO temporary overloading is_active field as a mean to confirm the email.
            # A better solution would be implement a profile model and add a is_email_confirmed
            # field there.
            user.is_active = False
            user.save()
            if user:
                url = reverse('activate_account',
                              kwargs={
                                  'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                  'token': account_activation_token.make_token(user)
                              },
                              request=request)
                message = f'''Hi {user.username},
Please click on the link to confirm your registration,

{url}'''
                send_mail('Confirm your email', message, from_email='localhost', recipient_list=[user.email])
                return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ActivateAccount(APIView):
    """API to activate account after signing-up.

    get:
    Confirm email address.
    """

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('Thank you for your email confirmation. Now you can login your account.',
                            status.HTTP_200_OK)
        else:
            return Response('Activation link is invalid!', status.HTTP_400_BAD_REQUEST)


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
