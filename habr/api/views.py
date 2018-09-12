import datetime

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from rest_framework import generics

from habr.api.serializers import *


class TopicList(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        limit = 100
        offset = 0
        if 'limit' in self.request.GET:
            limit = int(self.request.GET['limit'])
        if 'offset' in self.request.GET:
            offset = int(self.request.GET['offset'])

        return Topic.objects.all()[offset:offset + limit]


class TopicCreate(generics.CreateAPIView):
    serializer_class = TopicSerializer

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TopicLikeCreate(generics.CreateAPIView):
    serializer_class = TopicLikeSerializer

    def perform_create(self, serializer):
        timeout = 10
        topic_id = int(self.request.POST['topic_id'])
        user_id = self.request.user.id
        try:
            topic_like = TopicLike.objects.get(topic_id=topic_id, user_id=user_id)

            is_liked = True
        except Exception as e:

            is_liked = False
        topic = Topic.objects.get(id=topic_id)

        if is_liked:

            if (datetime.datetime.now().timestamp() - topic_like.created.timestamp()) < timeout:
                topic_like.delete()
                topic.number_of_likes -= 1

        else:

            topic.number_of_likes += 1
            serializer.save(user_id=self.request.user)
        topic.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        topic_id = int(self.request.POST['topic_id'])
        topic = Topic.objects.get(id=topic_id)
        topic.number_of_comments += 1
        topic.save()
        serializer.save(creator_id=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        limit = 100
        offset = 0
        if 'limit' in self.request.GET:
            limit = int(self.request.GET['limit'])
        if 'offset' in self.request.GET:
            offset = int(self.request.GET['offset'])

        return Comment.objects.all()[offset:offset + limit]


def jwt_response_payload_handler(request):
    authorization(request)
    return HttpResponse("ok")


def authorization(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_joined": user.date_joined
    })


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({
            'code': '200'
        })
    else:
        return JsonResponse({
            'code': '401'
        })
