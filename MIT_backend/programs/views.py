"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from rest_framework import viewsets

from .serializers import ProgramSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        user = self.request.user
        return user.mentee_programs.all()
