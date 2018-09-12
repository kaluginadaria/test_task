from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    number_of_comments = models.IntegerField(default=0)
    number_of_likes = models.IntegerField(default=0)
    creator_id = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Topic: ' + str(self.id)


class Comment(models.Model):
    body = models.TextField()
    creator_id = models.ForeignKey(User)
    topic_id = models.ForeignKey(Topic)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment: ' + str(self.id)


class TopicLike(models.Model):
    topic_id = models.ForeignKey(Topic)
    user_id = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'TopicLike: ' + str(self.id)
