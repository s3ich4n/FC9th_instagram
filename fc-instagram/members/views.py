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
    template = get_template('members/register.html')
    context = {}

    # TODO: 입력값에 대한 유효성 검증
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            login(request, user)
            return redirect('posts:post_list')
    else:
        form = RegisterForm()
        context['form'] = form
        return HttpResponse(template.render(context, request))
