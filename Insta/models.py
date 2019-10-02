from django.db import models

from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser

from django.urls import reverse

# Create your models here.

class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format = 'JPEG',
        options ={'quality':100},
        blank = True,
        null = True
    )

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections
    
    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers
    
    def is_followed_by(self,user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

class Post(models.Model):
    author = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='my_post'
    )
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
    )

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

    def get_like_count(self):
        return self.likes.count()


class PostTwo(models.Model):
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
        upload_to = 'staic/images/posts',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
    )




class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
        )
    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title

    class Meta:
        unique_together = ("post", "user")


class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set"
    )
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='friend_set'
    )

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='commnets',
    )
    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(
        auto_now_add=True,
        editable=False)

