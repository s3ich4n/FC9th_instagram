from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('upload/', views.post_create, name='post_create'),
]