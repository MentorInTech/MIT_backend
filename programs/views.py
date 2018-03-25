from rest_framework import generics
from .serializers import ProgramSerializer


class ProgramListView(generics.ListCreateAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        user = self.request.user
        return user.profile.program_set.all()


class ProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        user = self.request.user
        return user.profile.program_set.all()
