from django.urls import path

from . import views

app_name = 'members'
urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),
    path('profile/', views.profile_view, name='profile_view'),
    path('facebook-login/', views.facebook_login, name='facebook_login'),
]
