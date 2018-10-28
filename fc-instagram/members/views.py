from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import get_template

from .forms import LoginForm, RegisterForm, UserProfileForm


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

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()

    form = UserProfileForm(instance=request.user)
    context['form'] = form

    return HttpResponse(template.render(context, request))

