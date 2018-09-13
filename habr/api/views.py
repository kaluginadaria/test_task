import datetime

from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from habr.api.forms import AuthorizationForm
from habr.api.serializers import *


class TopicList(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TopicLikeCreate(generics.CreateAPIView):
    serializer_class = TopicLikeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        timeout = 10
        topic_id = int(self.request.POST['topic_id'])
        user_id = self.request.user.id
        try:
            topic_like = TopicLike.objects.get(topic_id=topic_id, user_id=user_id)

            is_liked = True
        except Exception as e:
            is_liked = False

        if is_liked:

            if (datetime.datetime.now().timestamp() - topic_like.created.timestamp()) < timeout:
                topic_like.delete()
                Topic.objects.filter(id=topic_id).update(number_of_likes=F('number_of_likes') - 1)
        else:
            Topic.objects.filter(id=topic_id).update(number_of_likes=F('number_of_likes') + 1)

            serializer.save(user_id=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        topic_id = int(self.request.POST['topic_id'])
        Topic.objects.filter(id=topic_id).update(number_of_comments=F('number_of_comments') + 1)
        serializer.save(creator_id=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        limit = 100
        offset = 0
        if 'limit' in self.request.GET:
            limit = int(self.request.GET['limit'])
        if 'offset' in self.request.GET:
            offset = int(self.request.GET['offset'])

        return Comment.objects.all()[offset:offset + limit]


def authorization(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthorizationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
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
            else:
                return JsonResponse({
                    'code': '401'
                })
    else:
        form = AuthorizationForm()

    return render(request, 'authorization.html', {'form': form})


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
