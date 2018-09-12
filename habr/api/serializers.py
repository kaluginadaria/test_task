from django.contrib.auth.models import User
from rest_framework import serializers

from habr.models import TopicLike, Topic, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')


class TopicSerializer(serializers.ModelSerializer):
    # creator_id = UserSerializer()

    class Meta:
        model = Topic
        fields = ('id', 'title', 'body', 'number_of_comments', 'number_of_likes', 'creator_id', 'created')
        read_only_fields = ['creator_id', 'number_of_comments', 'number_of_likes']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'creator_id', 'topic_id', 'created')
        read_only_fields = ['creator_id']


class TopicLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicLike
        fields = ('topic_id', 'user_id', 'created')
        read_only_fields = ['user_id']
