from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
from core.models import Team, User, Pod, Chore, Record
from .serializers import TeamSerializer, TeamCreateSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView

# Create your views here.
class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class TestView(APIView):
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data)

class TeamList(APIView):
    def get(self,request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

class TeamDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeamCreateSerializer
    permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)

    def get_queryset(self):
        return Team.objects.all()

# class UserDetialView(RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer

#     deg get_queryset(self):
#     return User.Objects.all()
