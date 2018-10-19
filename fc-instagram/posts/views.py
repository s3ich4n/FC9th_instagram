from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from posts.models import Post


def post_list(request):
    posts = Post.objects.all()
    template = get_template('posts/post_list.html')

    context = {'posts': posts}
    return HttpResponse(template.render(context, request))
