from rest_framework import serializers
from .models import User, Team, Chore, Assignment

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

class AssignmentDetailSerializer(serializers.ModelSerializer):
    chore = serializers.SlugRelatedField(queryset=Chore.objects.all(), slug_field='name')
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


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(read_only=True, many=True)
    captain = serializers.SlugRelatedField(read_only=True, slug_field='username')
    
    chores = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Team
        fields = [
            'pk',
            'name',
            'captain',
            'members',
            'background_image',
            'chores'
        ]

class TeamCreateSerializer(serializers.ModelSerializer):
    captain = serializers.SlugRelatedField(read_only=True, slug_field='username')
    members = MemberSerializer(read_only=True, many=True)
    chores = serializers.StringRelatedField(many=True, read_only=True)
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
            'chores'

        ]





class UserCreateSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'teams',
            "first_name",
            'last_name',
            "avatar",
            "assignments"
            
        ]

# class PointCountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model
