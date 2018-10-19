from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template

from .forms import UploadFileForm
from posts.models import Post


def post_list(request):
    posts = Post.objects.all()
    template = get_template('posts/post_list.html')

    context = {'posts': posts}
    return HttpResponse(template.render(context, request))


# https://docs.djangoproject.com/en/2.1/topics/http/file-uploads/
# 여기 참조.
def post_create(request):
    def handle_uploaded_file(f):
        with open(settings.MEDIA_ROOT, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    template = get_template('posts/post_create.html')
    context = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['image_file'])
            return HttpResponseRedirect('/success/url/')
    else:
        return HttpResponse(template.render(context, request))



