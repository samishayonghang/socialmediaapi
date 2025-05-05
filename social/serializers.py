from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile,Content,Comment,Like,Follow,Notification

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'
        read_only_fields = ['user']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'user', 'contentimage', 'caption', 'category', 'uploaddate']
        read_only_fields = ['user']
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']




class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  
    content = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'content', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    following = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'created_at']
class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.StringRelatedField() 
    sender = serializers.StringRelatedField()  
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_read'] 