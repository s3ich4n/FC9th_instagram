from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template


def post_list(request):
    template = get_template('posts/post_list.html')

    context = {}
    return HttpResponse(template.render(request, context))
