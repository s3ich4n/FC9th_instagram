import imghdr
import json
import requests
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import get_template

from .forms import LoginForm, RegisterForm, UserProfileForm


User = get_user_model()

# https://docs.djangoproject.com/en/2.1/ref/contrib/messages/
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#authenticating-users
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#how-to-log-a-user-in
def login_view(request):
    template = get_template('members/login.html')
    context = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('posts:post_list')
    else:
        form = LoginForm()

    context['form'] = form
    return HttpResponse(template.render(context, request))


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post_list')


def register_view(request):
    template = get_template('members/register.html')
    context = {}

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post_list')
    else:
        form = RegisterForm()

    # form 렌더링은 이런식으로
    context['form'] = form
    return HttpResponse(template.render(context, request))


@login_required
def profile_view(request):
    template = get_template('members/profile.html')
    context = {}

    # 인스턴스에는 수정할 유저를 인스턴스로 담아서 전달.
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            # https://docs.djangoproject.com/en/2.1/ref/contrib/messages/
            # is_valid()를 통과하고 인스턴스 수정이 완료되면
            # messages모듈을 사용해서 템플릿에 수정완료 메시지를 표시
            messages.success(request, '프로필 수정이 완료되었습니다.')

    form = UserProfileForm(instance=request.user)
    context['form'] = form

    return HttpResponse(template.render(context, request))


def facebook_login(request):
    user = authenticate(request, facebook_request_token=request.GET.get('code'))
    if user:
        login(request, user)
        return redirect('posts:post_list')
    messages.error(request, '페이스북 로그인에 실패하였습니다.')
    return redirect('members:login_view')

