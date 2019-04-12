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

class SignupSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required = False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = None
        if validated_data.get('profile') is not None:
            profile_data = validated_data.pop('profile')

        user = User(
            email = validated_data['email'], 
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        if profile_data is None:
            UserProfile.objects.create(user=user, role='USER')
        else:
            UserProfile.objects.create(user=user, **profile_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required = False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if validated_data.get('profile') is not None:
            instance.profile.role = validated_data['profile']['role']
            instance.profile.save()
            
        return instance

class EntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField()
    class Meta:
        model = Entry
        fields = ('id', 'distance', 'duration', 'date', 'user', 'user_id')
        read_only_fields = ('user',)
        write_only_fields = ('user_id',)