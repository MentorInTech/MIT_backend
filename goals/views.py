from rest_framework import generics
from .serializers import GoalSerializer


class GoalView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer

    def get_queryset(self):
        user = self.request.user
        return user.profile.goal_set.all()
