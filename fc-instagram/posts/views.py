import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template


# from members.models import User
from .models import Post, Comment, Hashtags
from .forms import UploadFileForm, CommentCreateForm, CommentForm, PostForm


def post_list(request):
    posts = Post.objects.all()
    template = get_template('posts/post_list.html')

    context = {
        'posts': posts,
        'comment_form': CommentCreateForm(),
    }
    return HttpResponse(template.render(context, request))


@login_required
def post_create(request):
    template = get_template('posts/post_create.html')
    context = {}

    # 로그인 확인 로직
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # request.FILES에 form에서 보낸 파일객체가 들어있음
        # 새로운 Post를 생성한다.
        #  author는 User.objects.first()
        #  photo는 request.FILES에 있는 내용을 적절히 꺼내서 쓴다
        # 완료된 후 posts:post_list로 redirect
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            comment_content = form.cleaned_data['comment']
            if comment_content:
                post.comments.create(
                    author=request.user,
                    context=comment_content,
                )

            return redirect('posts:post_list')

    else:
        # GET으로 오면 빈 Form 인스턴스를 context에 담아 전달.
        # Template에서는 'form'키로 Form 인스턴스 속성을 사용함.
        form = PostForm()

    context['form'] = form
    return HttpResponse(template.render(context, render))


def comment_create(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        # 댓글 작성 form 형태에서 값 받아옴.
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # 댓글 저장 후, content에 포함된 Hashtags 목록을
            # 댓글의 tags 속성에 set한다.
            p = re.compile(r'#(?P<tag>\w+)')
            hashtags = [Hashtags.objects.get_or_create(tag_name=tag_name)[0]
                        for tag_name in re.findall(p, comment.contents)]
            comment.hashtags.set(hashtags)

            return redirect('posts:post_list')

