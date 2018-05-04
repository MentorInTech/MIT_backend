"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Mentor
from .serializers import MentorNoLoginSerializer, MentorWithLoginSerializer


class MentorPublicViewSet(ReadOnlyModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = Mentor.objects.all()
    serializer_class = MentorNoLoginSerializer


class MentorMemberOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorWithLoginSerializer
