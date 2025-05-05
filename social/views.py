from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from social.serializers import UserSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Profile,Content,Comment,Like,Follow
from.serializers import ProfileSerializer,ContentSerializer,CommentSerializer,FollowSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .tasks import send_notification

# Create your views here.
class RegisterView(APIView):
    permission_classes =[AllowAny]
    def post(self, request):
       
        
        serializer = UserSerializer(data=request.data)
        
    
        if serializer.is_valid():
            user = serializer.save() 
            
            return Response({
                'message': 'User created successfully.',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
       

        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')

        try:
            user=User.objects.get(username=username)
            if user.check_password(password):
                refresh=RefreshToken.for_user(user)
                return Response({
                    'message':'Login successfully',
                    'access_token':str(refresh.access_token),
                    'refresh_token':str(refresh),
                },status=status.HTTP_200_OK)
            return Response({'detail':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail':'User not found'},status=status.HTTP_404_NOT_FOUND)
        

class ProfileListView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

class MyProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        if Profile.objects.filter(user=request.user).exists():
            return Response({'error': 'Profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ContentListAPIView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        
        content = Content.objects.all()
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

class ContentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, content_id, user):
       
        try:
            content = Content.objects.get(id=content_id, user=user)
            return content
        except Content.DoesNotExist:
            return None
    
  
  

    def put(self, request, content_id):
       
        content = self.get_object(content_id, request.user)
        if content:
            serializer = ContentSerializer(content, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Content not found or you do not have permission to update it.'},
                        status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, content_id):
        content = self.get_object(content_id, request.user)
        if content:
            serializer = ContentSerializer(content, data=request.data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Content not found or you do not have permission to update it.'},
                        status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, content_id):
       
        content = self.get_object(content_id, request.user)
        if content:
            content.delete()
            return Response({'detail': 'Content deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Content not found or you do not have permission to delete it.'},
                        status=status.HTTP_404_NOT_FOUND)
    


class CommentCreateListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, content_id):
        comments = Comment.objects.filter(content_id=content_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, content_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, content_id=content_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, comment_id, user):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != user:
            return None
        return comment

    def put(self, request, comment_id):
        comment = self.get_object(comment_id, request.user)
        if comment:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not allowed to edit this comment'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, comment_id):
        comment = self.get_object(comment_id, request.user)
        if comment:
            comment.delete()
            return Response({'detail': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not allowed to delete this comment'}, status=status.HTTP_403_FORBIDDEN)
    

class ToggleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, content_id):
        content = get_object_or_404(Content, id=content_id)
        user = request.user

        
        like, created = Like.objects.get_or_create(user=user, content=content)

        if not created:
            like.delete()
            message = "Unliked"
        else:
            message = "Liked"

        
        like_count = content.likes.count()
        usernames = list(content.likes.select_related('user').values_list('user__username', flat=True))

        return Response({
            "message": message,
            "like_count": like_count,
            "liked_users": usernames
        }, status=status.HTTP_200_OK)
    


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=404)

        if user_to_follow == request.user:
            return Response({'detail': 'You cannot follow yourself'}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=user_to_follow
        )
        if created:
            return Response({'detail': f'You are now following {username}'}, status=201)
        else:
            return Response({'detail': f'You are already following {username}'}, status=200)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, username):
        try:
            user_to_unfollow = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=404)

        try:
            follow = Follow.objects.get(follower=request.user, following=user_to_unfollow)
            follow.delete()
            return Response({'detail': f'You unfollowed {username}'}, status=204)
        except Follow.DoesNotExist:
            return Response({'detail': 'You are not following this user'}, status=400)


class FollowersListView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.user = User.objects.get(username=self.kwargs['username'])
        return Follow.objects.filter(following=self.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "followers": serializer.data
        })


class FollowingListView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.user = User.objects.get(username=self.kwargs['username'])
        return Follow.objects.filter(follower=self.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "following": serializer.data
        })
    
class CreateNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        action = request.data.get('action')  # 'like', 'comment', 'like_comment', 'reply_comment'
        content_id = request.data.get('content_id')
        comment_id = request.data.get('comment_id')
        comment_text = request.data.get('comment_text', '')

        sender = request.user
        message = ""
        recipient = None

        if action == 'like':
            # Like on a content post
            try:
                content = Content.objects.get(id=content_id)
                recipient = content.user
                if recipient != sender:
                    Like.objects.get_or_create(user=sender, content=content)
                    message = f"{sender.username} liked your post."
            except Content.DoesNotExist:
                return Response({'error': 'Content not found'}, status=404)

        elif action == 'comment':
            # Comment on a content post
            try:
                content = Content.objects.get(id=content_id)
                recipient = content.user
                if recipient != sender:
                    Comment.objects.create(user=sender, content=content, text=comment_text)
                    message = f"{sender.username} commented: '{comment_text}'"
            except Content.DoesNotExist:
                return Response({'error': 'Content not found'}, status=404)

        elif action == 'like_comment':
            # Like on a comment
            try:
                comment = Comment.objects.get(id=comment_id)
                recipient = comment.user
                if recipient != sender:
                    # You could add LikeOnComment model if needed
                    message = f"{sender.username} liked your comment: '{comment.text[:30]}...'"
            except Comment.DoesNotExist:
                return Response({'error': 'Comment not found'}, status=404)

        elif action == 'reply_comment':
            # Reply to a comment
            try:
                parent_comment = Comment.objects.get(id=comment_id)
                recipient = parent_comment.user
                if recipient != sender:
                    # Save reply (optional: create a Reply model if needed)
                    Comment.objects.create(user=sender, content=parent_comment.content, text=comment_text)
                    message = f"{sender.username} replied to your comment: '{comment_text}'"
            except Comment.DoesNotExist:
                return Response({'error': 'Parent comment not found'}, status=404)

        else:
            return Response({'error': 'Invalid action'}, status=400)

        if recipient and message:
            send_notification.delay(sender.id, recipient.id, message)
            return Response({'message': 'Notification will be sent'}, status=201)

        return Response({'message': 'No notification sent (self-action or missing target).'}, status=200)