from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('',
         views.post_list,
         name='post_list'),
    path('upload/',
         views.post_create,
         name='post_create'),
    # post의 pk를 찾을 때 이렇게 함.
    path('<int:post_pk>/comments/create/',
         views.comment_create,
         name='comment_create'),
    path('tag_search/',
         views.tag_search,
         name='tag_search'),
    path('<int:post_pk>/like_toggle/',
         views.post_like_toggle,
         name='post_like_toggle'),
]
