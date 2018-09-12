from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'^topic.list$', TopicList.as_view()),
    url(r'^topic.create$', TopicCreate.as_view()),
    url(r'^topic.like$', TopicLikeCreate.as_view()),
    url(r'^comment.create$', CommentCreate.as_view()),
    url(r'^comment.list$', CommentList.as_view()),
    url(r'^auth.login$',authorization),
    url(r'^auth.logout$', logout_view)
]
