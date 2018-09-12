from django.contrib import admin

from .models import Topic,TopicLike,Comment,User

admin.site.register(Topic)
admin.site.register(TopicLike)
admin.site.register(Comment)
