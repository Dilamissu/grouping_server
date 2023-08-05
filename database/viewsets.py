from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny
from .models import Activity, User, Workspace, MissionState
from .serializers import ActivitySerializer, UserSerializer, WorkspaceSerializer, MissionStateSerializer, ActivityPatchSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ActivityPatchSerializer
        return super().get_serializer_class()


class MissionStateViewSet(viewsets.ModelViewSet):
    queryset = MissionState.objects.all()
    serializer_class = MissionStateSerializer
