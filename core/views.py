from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
from core.models import Team, User, Pod, Chore, Assignment
from .serializers import TeamSerializer, TeamCreateSerializer, ChoreSerializer, AssignmentSerializer, UserCreateSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView

# Create your views here.
class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == user

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


class UserAssignmentView(APIView):
    def get(self,request,username):
        lookup_field = 'username'
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all()
        serializer = AssignmentSerializer(queryset, many=True)
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


class TeamCreateListView(ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer
    def perform_create(self, serializer):
        serializer.save(captain=self.request.user)

    def get(self,request):
        teams = Team.objects.all()
        serializer = TeamCreateSerializer(teams, many=True)
        return Response(serializer.data)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserCreateSerializer
    # permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)
    lookup_field = 'username'
    def get_queryset(self):
        return User.objects.all()

class AssignmentCreateListView(ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    def perform_create(self, serializer):
        serializer.save()

    def get(self,request):
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)


class ChoreCreateListView(ListCreateAPIView):
    
    queryset = Chore.objects.all()
    serializer_class = ChoreSerializer
    def perform_create(self, serializer):
        serializer.save()

    def get(self,request):
        chores = Chore.objects.all()
        serializer = ChoreSerializer(chores, many=True)
        return Response(serializer.data)


class ChoreDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ChoreSerializer
    # permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)

    def get_queryset(self):
        return Chore.objects.all()

class AssignmentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    # permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)

    def get_queryset(self):
        return Assignment.objects.all()