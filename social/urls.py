from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from social.views import RegisterView,LoginView,ProfileListView,MyProfileView,ContentListAPIView,ContentCreateAPIView,ContentDetailAPIView,CommentCreateListView,CommentDetailView,ToggleLikeAPIView,FollowersListView,FollowingListView,FollowUserView,UnfollowUserView,CreateNotificationView
urlpatterns = [
    path('social/notifications/create/', CreateNotificationView.as_view(), name='create-notification'),
    path('social/followers/<str:username>/', FollowUserView.as_view(), name='followers-list'),
    path('social/unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow-user'),

    path('social/<str:username>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('social/<str:username>/following/', FollowingListView.as_view(), name='following-list'),

    path('social/content/<int:content_id>/comments/', CommentCreateListView.as_view(), name='comment-list-create'),
    path('social/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
    path('social/content/', ContentListAPIView.as_view(), name='content-list'),  
    path('social/content/create/', ContentCreateAPIView.as_view(), name='content-create'),  
    path('social/content/<int:content_id>/', ContentDetailAPIView.as_view(), name='content-detail'),  
    path('social/profile/',ProfileListView.as_view()),
    path('social/myprofile/',MyProfileView.as_view()),
    path('social/login/',LoginView.as_view(),name='login'),
    path('social/register/',RegisterView.as_view(),name='register'),
    path('social/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('social/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('social/content/<int:content_id>/like/', ToggleLikeAPIView.as_view(), name='toggle-like'),

]

