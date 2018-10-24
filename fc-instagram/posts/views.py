from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template


# from members.models import User
from .forms import UploadFileForm
from posts.models import Post


def post_list(request):
    posts = Post.objects.all()
    template = get_template('posts/post_list.html')

    context = {
        'posts': posts,
    }
    return HttpResponse(template.render(context, request))


# https://docs.djangoproject.com/en/2.1/topics/http/file-uploads/
# 여기 참조.
# Post.objects.all() 이기 때문에 못 불러오는데,
# 유저 로그인한 시점에서 이걸 하면 저걸 쓰고도 불러오게 하고싶다
# 그렇다면, 로그인 구현+디비추가 까지 같이 해야하나?
@login_required
def post_create(request):
    template = get_template('posts/post_create.html')
    context = {}

    # 로그인 확인 로직
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # request.FILES에 form에서 보낸 파일객체가 들어있음
        # 새로운 Post를 생성한다.
        #  author는 User.objects.first()
        #  photo는 request.FILES에 있는 내용을 적절히 꺼내서 쓴다
        # 완료된 후 posts:post_list로 redirect
        if form.is_valid():
            form.save(author=request.user)
            return redirect('posts:post_list')

    else:
        # GET으로 오면 빈 Form 인스턴스를 context에 담아 전달.
        # Template에서는 'form'키로 Form 인스턴스 속성을 사용함.
        form = UploadFileForm()

    context['form'] = form
    return HttpResponse(template.render(context, render))
