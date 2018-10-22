from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template


# from members.models import User
from .forms import UploadFileForm
from posts.models import Post


def post_list(request):
    posts = Post.objects.all()
    template = get_template('posts/post_list.html')

    context = {'posts': posts}
    return HttpResponse(template.render(context, request))


# https://docs.djangoproject.com/en/2.1/topics/http/file-uploads/
# 여기 참조.
# TODO: 질문하기!
# Post.objects.all() 이기 때문에 못 불러오는데,
# 유저 로그인한 시점에서 이걸 하면 저걸 쓰고도 불러오게 하고싶다
# 그렇다면, 로그인 구현+디비추가 까지 같이 해야하나?
def post_create(request):

    template = get_template('posts/post_create.html')
    context = {}
    if request.method == 'POST' and request.FILES['uploaded_image']:
        uploaded = request.FILES['uploaded_image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded.name, uploaded)
        uploaded_file_url = fs.url(filename)
        # SessionMiddleware
        # AuthenticationMiddleware
        #   를 통해서 request의 user 속성에
        #   해당 사용자 인스턴스가 할당
        post = Post(
            author=request.User,
            photo=request.FILES['uploaded_image'],
        )
        post.save()

        return render(request, 'posts/post_create.html', {
            'uploaded_file_url': uploaded_file_url
        })
    else:
        form = UploadFileForm()
        return HttpResponse(template.render({'form': form}, request))



