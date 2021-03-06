from rest_framework import serializers
from .models import User, Team, Chore, Assignment, Pod, Feed, Notification
from django.db.models import Sum


class AvatarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'username',
            'avatar',
            'teams'
        ]
class ChoreSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='name')
    
    class Meta:
        model = Chore
        fields = [
            'pk',
            'name',
            'detail',
            'points',
            'team'

        ]

    

class AssignmentSerializer(serializers.ModelSerializer):
    queryset = Chore.objects.all()
    chore = ChoreSerializer(queryset)
    # chore = serializers.SlugRelatedField(queryset=Chore.objects.all(), slug_field='name')
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    

    class Meta:
        model = Assignment
        
        fields = [
            'user',
            'pk',
            'chore',
            'comment',
            'assignment_type',
            'complete',
        ]
class NotificationSerializer(serializers.ModelSerializer):
    sender = AvatarSerializer(read_only=True)
    target = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Notification
        fields = [
            'feed',
            'sender',
            'target',
            'message',
            'emoji',
            'notification_type'
        ]
    
class FeedSerializer(serializers.ModelSerializer):
    notifications = NotificationSerializer(many=True, read_only=True)
    class Meta:
        model = Feed 
        fields = [
            'pk',
            'pod',
            'team',
            'user',
            'notifications'
        ]    
    
            
            
        
    
        

class AssignmentDetailSerializer(serializers.ModelSerializer):
    # chore = serializers.SlugRelatedField(queryset=Chore.objects.all(), slug_field='name')
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = Assignment
        fields = [
            'user',
            'pk',
            'chore',
            'comment',
            'assignment_type',
            'complete',
        ]
   

class UserSerializer(serializers.ModelSerializer):
    chores = serializers.StringRelatedField(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    teams = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'teams',
            'chores',
            'assignments',
            
        ]

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'avatar',
        ]

class UserCreateSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    possible_chore_points = serializers.SerializerMethodField()
    earned_chore_points = serializers.SerializerMethodField()
    monday_chore_points = serializers.SerializerMethodField()
    tuesday_chore_points = serializers.SerializerMethodField()
    wednesday_chore_points = serializers.SerializerMethodField()
    thursday_chore_points = serializers.SerializerMethodField()
    friday_chore_points = serializers.SerializerMethodField()
    saturday_chore_points = serializers.SerializerMethodField()
    sunday_chore_points = serializers.SerializerMethodField()
    monday_possible_points = serializers.SerializerMethodField()
    tuesday_possible_points = serializers.SerializerMethodField()
    wednesday_possible_points = serializers.SerializerMethodField()
    thursday_possible_points = serializers.SerializerMethodField()
    friday_possible_points = serializers.SerializerMethodField()
    saturday_possible_points = serializers.SerializerMethodField()
    sunday_possible_points = serializers.SerializerMethodField()
    feed = FeedSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'teams',
            "first_name",
            'last_name',
            "avatar",
            "assignments",
            'user_type',
            'feed',
            'possible_chore_points',
            'earned_chore_points',
            'monday_chore_points',
            'tuesday_chore_points',
            'wednesday_chore_points',
            'thursday_chore_points',
            'friday_chore_points',
            'saturday_chore_points',
            'sunday_chore_points',
            'monday_possible_points',
            'tuesday_possible_points',
            'wednesday_possible_points',
            'thursday_possible_points',
            'friday_possible_points',
            'saturday_possible_points',
            'sunday_possible_points'
            ]
    def get_possible_chore_points(self,obj):
        return obj.assignments.aggregate(Sum('chore__points'))
        
    def get_earned_chore_points(self,obj):
        return obj.assignments.filter(complete=True).aggregate(Sum('chore__points'))

    def get_monday_chore_points(self,obj):
        return obj.assignments.exclude(complete=False).filter(assignment_type='MONDAY').aggregate(Sum('chore__points', null=0))
    
    def get_tuesday_chore_points(self,obj):
        return obj.assignments.exclude(complete=False).filter(assignment_type='TUESDAY').aggregate(Sum('chore__points'))

    def get_wednesday_chore_points(self,obj):
        return obj.assignments.exclude(complete=False).filter(assignment_type='WEDNESDAY').aggregate(Sum('chore__points'))

    def get_thursday_chore_points(self,obj):
        return obj.assignments.exclude(complete=False).filter(assignment_type='THURSDAY').aggregate(Sum('chore__points'))

    def get_friday_chore_points(self,obj):
        return obj.assignments.exclude(complete=False).filter(assignment_type='FRIDAY').aggregate(Sum('chore__points'))

    def get_saturday_chore_points(self,obj):
        return obj.assignments.exclude(complete=False).filter(assignment_type='SATURDAY').aggregate(Sum('chore__points'))

    def get_sunday_chore_points(self,obj):
        return obj.assignments.exclude(complete=False).filter(assignment_type='SUNDAY').aggregate(Sum('chore__points'))
    
    def get_monday_possible_points(self,obj):
        return obj.assignments.filter(assignment_type='MONDAY').aggregate(Sum('chore__points', null=0))

    def get_tuesday_possible_points(self,obj):
        return obj.assignments.filter(assignment_type='TUESDAY').aggregate(Sum('chore__points', null=0))
    
    def get_wednesday_possible_points(self,obj):
        return obj.assignments.filter(assignment_type='WEDNESDAY').aggregate(Sum('chore__points', null=0))

    def get_thursday_possible_points(self,obj):
        return obj.assignments.filter(assignment_type='THURSDAY').aggregate(Sum('chore__points', null=0))

    def get_friday_possible_points(self,obj):
        return obj.assignments.filter(assignment_type='FRIDAY').aggregate(Sum('chore__points', null=0))

    def get_saturday_possible_points(self,obj):
        return obj.assignments.filter(assignment_type='SATURDAY').aggregate(Sum('chore__points', null=0))

    def get_sunday_possible_points(self,obj):
        return obj.assignments.filter(assignment_type='SUNDAY').aggregate(Sum('chore__points', null=0))

   


class TeamSerializer(serializers.ModelSerializer):
    members = UserCreateSerializer(read_only=True, many=True)
    captain = serializers.SlugRelatedField(read_only=True, slug_field='username')
    pods = serializers.StringRelatedField(many=True, read_only=True)
    chores = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Team
        fields = [
            'pk',
            'name',
            'captain',
            'members',
            'background_image',
            'chores',
            'pods'
        ]

    
    

class TeamCreateSerializer(serializers.ModelSerializer):
    captain = serializers.SlugRelatedField(read_only=True, slug_field='username')
    members = UserCreateSerializer(read_only=True, many=True)
    chores = serializers.StringRelatedField(many=True, read_only=True)
    pods = serializers.StringRelatedField(many=True, read_only=True)
    feed = FeedSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'pk',
            'name',
            'slogan',
            'captain',
            'members',
            'theme_song',
            'background_image',
            'dashboard_style',
            'chores',
            'pods',
            'feed',
            

        ]
    





 


class PodSerializer(serializers.ModelSerializer):
    teams = TeamCreateSerializer(many=True, read_only=True)
    feed = FeedSerializer(many=True, read_only=True)
    class Meta:
        model = Pod
        fields = [
            'pk',
            'name',
            'teams',
            'feed'
        ]

class PodCreateSerializer(serializers.ModelSerializer):
    teams = serializers.StringRelatedField(many=True, read_only=True)
    feed = FeedSerializer(many=True, read_only=True)
    class Meta:
        model = Pod
        fields = [
            'pk',
            'name',
            'teams',
            'feed'
        ]





