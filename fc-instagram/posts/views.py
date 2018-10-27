import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template


# from members.models import User
from .models import Post
from .forms import CommentForm, PostForm


def post_list(request):
    posts = Post.objects.all()
    template = get_template('posts/post_list.html')

    context = {
        'posts': posts,
        'comment_form': CommentForm(),
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

            return redirect('posts:post_list')


def tag_post_list(request, tag_name):
    # 포스트 중, 자신에게 속한 comment 가 가진 '유일한' Hashtags 목록 중
    # tag_name이 name인 Hashtags가 포함된
    # Post 목록을 posts 변수에 할당
    # context에 담아서 render 수행.
    # HTML: /posts/tag_post_list.html
    template = get_template('posts/tag_post_list.html')
    posts = Post.objects.filter(
        comments__hashtags__tag_name=tag_name).distinct()
    context = {
        'posts': posts,
    }
    return HttpResponse(template.render(context, request))


def tag_search(request):
    # request.GET으로 전달된
    #  search_keyword값을 적절히 활용해서
    #  위의 tag_post_list view로 redirect
    # URL: '/posts/tag-search/'
    # URL Name: 'posts:tag-search'
    # Template: 없음
    search_keyword = request.GET.get('search_keyword')
    substituted_keyword = re.sub(r'#|\s+', '', search_keyword)
    return redirect('tag_post_list', substituted_keyword)
