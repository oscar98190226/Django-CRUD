from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Entry, UserProfile

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'role')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data['email'], 
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(
            user = user,
            role = 'USER'
        )
        return user

class EntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    class Meta:
        model = Entry
        fields = ('id', 'distance', 'duration', 'date', 'user', 'user_id')
        read_only_fields = ('user',)
        write_only_fields = ('user_id',)