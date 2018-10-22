from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

from .forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        pass
    else:
        template = get_template('members/login.html')
        form = LoginForm()
        context = {
            'form': form,
        }

        return HttpResponse(template.render(context, request))
