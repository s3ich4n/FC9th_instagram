from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template

from .forms import LoginForm, RegisterForm


# https://docs.djangoproject.com/en/2.1/topics/auth/default/#authenticating-users
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#how-to-log-a-user-in
# TODO: 에러처리 수업때 한 소스코드로 공부해오기!
def login_view(request):
    template = get_template('members/login.html')
    form = LoginForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
            return redirect('posts:post_list')
        else:
            context['error'] = 'error'
            return HttpResponse(template.render(context, request))

    else:
        context = {
            'form': form,
        }

        return HttpResponse(template.render(context, request))


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post_list')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # 이렇게 짜야 exists로 바로 있는지없는지 테스트함!
        if User.objects.filter(username=username).exists():
            return HttpResponse(f'사용자명 {username}이 이미 있음.')
        if password != password_confirm:
            return HttpResponse(f'비번 확인하셈')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            user.save()
            return redirect('posts:post_list')

    else:
        template = get_template('members/register.html')
        form = RegisterForm()
        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))
