from rest_framework import serializers
from .models import User, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
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