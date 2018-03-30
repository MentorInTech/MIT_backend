from rest_framework import viewsets

from .serializers import ProgramSerializer
from .models import Program


class ProgramViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        user = self.request.user
        return user.mentee_programs.all()
