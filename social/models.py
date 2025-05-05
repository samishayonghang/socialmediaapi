from django.db import models
from django.contrib.auth.models import User

STATE_CHOICE=((
    ('koshi', 'Koshi'),
    ('madhesh', 'Madhesh'),
    ('bagmati', 'Bagmati'),
    ('gandaki', 'Gandaki'),
    ('lumbini', 'Lumbini'),
    ('karnali', 'Karnali'),
    ('sudurpaschim', 'Sudurpaschim'),
))
CATEGORY_CHOICES = (
    ('travel', 'Travel'),
    ('food', 'Food'),
    ('lifestyle', 'Lifestyle'),
    ('technology', 'Technology'),
    ('art', 'Art'),
    ('nature', 'Nature'),
    ('education', 'Education'),
    ('sports', 'Sports'),
    ('fashion', 'Fashion'),
    ('news', 'News'),
    ('personal', 'Personal'),
    ('motivational', 'Motivational'),
    ('entertainment', 'Entertainment'),
    ('health', 'Health'),
    ('others', 'Others'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pimg=models.ImageField(upload_to='profileimage/',blank=True)
    location=models.CharField(choices=STATE_CHOICE,max_length=50)
    bio=models.CharField(max_length=100)
    workplace=models.CharField(max_length=100)

class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    contentimage=models.ImageField(upload_to='contentimage/')
    caption=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    uploaddate=models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey('content', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey('content', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user.username} liked {self.content.id}"
    

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)