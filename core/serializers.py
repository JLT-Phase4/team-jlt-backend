from rest_framework import serializers
from .models import User, Team, Chore, Record

class AvatarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'username',
            'avatar',
            'teams'
        ]

class RecordSerializer(serializers.ModelSerializer):
    chore = serializers.SlugRelatedField(read_only=True, slug_field='name')
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Record
        fields = [
            'user',
            'pk',
            'chore',
            'date',
            'comment',
            'complete',
        ]

class UserSerializer(serializers.ModelSerializer):
    chores = serializers.StringRelatedField(many=True, read_only=True)
    records = RecordSerializer(many=True, read_only=True)
    teams = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'teams',
            'chores',
            'records',
            
        ]


class TeamSerializer(serializers.ModelSerializer):
    captain = serializers.SlugRelatedField(read_only=True, slug_field='username')
    members = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Team
        fields = [
            'pk',
            'name',
            'captain',
            'members',
            'background_image'
        ]

class TeamCreateSerializer(serializers.ModelSerializer):
    captain = serializers.SlugRelatedField(read_only=True, slug_field='username')
    members = serializers.StringRelatedField(many=True, read_only=True)
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
            'dashboard_style'

        ]


class UserChoreSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    user = AvatarSerializer(read_only=True)
    
    class Meta:
        model = Chore
        fields = [
            'pk',
            'user',
            'name',
            'detail',
            'chore_type',

        ]

