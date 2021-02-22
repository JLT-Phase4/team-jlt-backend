from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
from core.models import Team, User, Pod, Chore, Record
from .serializers import TeamSerializer, TeamCreateSerializer, UserChoreSerializer, RecordSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView

# Create your views here.
class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class LoggedInUserView(APIView):
    def get(self,request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(data=serializer.data)

class AllUserView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    def get(self,request,username):
        lookup_field = 'username'
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)


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

class UserChoreDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserChoreSerializer

    def get_queryset(self):
        return Chore.objects.all()


class UserChoreView(APIView):
    def get(self,request, username):
        lookup_field = 'username'
        user = get_object_or_404(User, username=username)
        queryset = user.chores.all()
        serializer = UserChoreSerializer(queryset, many=True)
        return Response(serializer.data)



class RecordDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RecordSerializer
    # permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)

    def get_queryset(self):
        return Record.objects.all()


class RecordView(APIView):
    def get(self,request):
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)
    

class TeamListView(APIView):
    
    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamCreateSerializer(team)
        return Response(serializer.data)

    def post(self, request, pk):
        new_team_member_username = request.data.get('username')
        team = get_object_or_404(Team, pk=pk)
        
        if not new_team_member_username:
            raise ParseError("No username provided")
        
        user = User.objects.filter(username=new_team_member_username).first()
        if user is None:
            raise ParseError(f"User {new_team_member_username} does not exist")
        
        team.members.add(user)
        
        serializer = TeamCreateSerializer(team)
        return Response(serializer.data)

    def delete(self, request, pk):
        delete_member_username = request.data.get('username')
        team = get_object_or_404(Team, pk=pk)
        if not delete_member_username:
            raise ParseError("No username provided")

        user = User.objects.filter(username=delete_member_username).first()
        if user is None:
            raise ParseError(f"User {delete_member_username} does not exist")

        team.members.remove(user)
        
        serializer = TeamSerializer(team)
        return Response(serializer.data)