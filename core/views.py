from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.db.models import Sum
from core.models import Team, User, Pod, Chore, Assignment, Feed, Notification
from .serializers import TeamSerializer, TeamCreateSerializer, ChoreSerializer, AssignmentSerializer, UserCreateSerializer, AssignmentDetailSerializer, PodSerializer, PodCreateSerializer, FeedSerializer, NotificationSerializer
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
    serializer_class = AssignmentDetailSerializer
    def perform_create(self, serializer):
        serializer.save()

    def get(self,request):
        assignments = Assignment.objects.all()
        serializer = AssignmentDetailSerializer(assignments, many=True)
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
    serializer_class = AssignmentDetailSerializer
    # permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)

    def get_queryset(self):
        return Assignment.objects.all()



class PointCountView(APIView):
    lookup_field = 'username'
    # serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        total_points = user.assignments.all().exclude(complete=False).aggregate(Sum('chore__points'))
        return Response(total_points)


class PodDetailView(APIView):
    def get(self,request,pk):
        pod = get_object_or_404(Pod, pk=pk)
        serializer = PodSerializer(pod)
        return Response(serializer.data)



class PodListView(APIView):
    
    def get(self, request, pk):
        pod = get_object_or_404(Pod, pk=pk)
        serializer = PodCreateSerializer(pod)
        return Response(serializer.data)

    def post(self, request, pk):
        new_team = request.data.get('name')
        pod = get_object_or_404(Pod, pk=pk)
        
        if not new_team:
            raise ParseError("No Team provided")
        
        team = Team.objects.filter(name=new_team).first()
        if team is None:
            raise ParseError(f"Team {new_team} does not exist")
        
        pod.teams.add(team)
        
        serializer = PodCreateSerializer(pod)
        return Response(serializer.data)

    def delete(self, request, pk):
        delete_team = request.data.get('name')
        pod = get_object_or_404(Pod, pk=pk)
        if not delete_team:
            raise ParseError("No Team provided")

        team = Team.objects.filter(name=delete_team).first()
        if team is None:
            raise ParseError(f"Team {delete_team} does not exist")

        pod.teams.remove(team)
        
        serializer = PodCreateSerializer(pod)
        return Response(serializer.data)

class PodCreateView(ListCreateAPIView):
    queryset = Pod.objects.all()
    serializer_class = PodCreateSerializer
    def perform_create(self, serializer):
        serializer.save()

    def get(self,request):
        pods = Pod.objects.all()
        serializer = PodSerializer(pods, many=True)
        return Response(serializer.data)


class MondayPointCount(APIView):
    lookup_field = 'username'
    serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all().exclude(complete=False).filter(assignment_type="MONDAY").aggregate(Sum('chore__points'))
        return Response(queryset)

class TuesdayPointCount(APIView):
    lookup_field = 'username'
    serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all().exclude(complete=False).filter(assignment_type="TUESDAY").aggregate(Sum('chore__points'))
        return Response(queryset)

class WednesdayPointCount(APIView):
    lookup_field = 'username'
    serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all().exclude(complete=False).filter(assignment_type="WEDNESDAY").aggregate(Sum('chore__points'))
        return Response(queryset)

class ThursdayPointCount(APIView):
    lookup_field = 'username'
    serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all().exclude(complete=False).filter(assignment_type="THURSDAY").aggregate(Sum('chore__points'))
        return Response(queryset)

class FridayPointCount(APIView):
    lookup_field = 'username'
    serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all().exclude(complete=False).filter(assignment_type="FRIDAY").aggregate(Sum('chore__points'))
        return Response(queryset)

class SaturdayPointCount(APIView):
    lookup_field = 'username'
    serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all().exclude(complete=False).filter(assignment_type="SATURDAY").aggregate(Sum('chore__points'))
        return Response(queryset)

class SundayPointCount(APIView):
    lookup_field = 'username'
    serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all().exclude(complete=False).filter(assignment_type="SUNDAY").aggregate(Sum('chore__points'))
        return Response(queryset)

class AnyPointCount(APIView):
    lookup_field = 'username'
    serializer_class = AssignmentSerializer
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        queryset = user.assignments.all().exclude(complete=False).filter(assignment_type="ANY").aggregate(Sum('chore__points'))
        return Response(queryset)

class AllFeedView(APIView):
    def get(self,request):
        feeds = Feed.objects.all()
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data)




class NotificationCreateView(ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get(self,request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class FeedCreateView(ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    def perform_create(self, serializer):
        serializer.save()

    def get(self,request):
        feeds = Feed.objects.all()
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data)