from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from .forms import PostForm
from django.conf import settings
from django.contrib.auth.decorators import login_required


def get_page_context(queryset, request):
    paginator = Paginator(queryset, settings.POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }


def index(request):
    template = 'posts/index.html'
    title = 'Это главная страница проекта Yatube'
    post_list = Post.objects.select_related('author', 'group').all()
    context = {
        'title': title,
    }
    context.update(get_page_context(post_list, request))
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    post_list = group.posts.select_related('group').all()
    context = {
        'group': group,
    }
    context.update(get_page_context(post_list, request))
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('author').all()
    posts_count = author.posts.select_related('author').count()
    context = {
        'author': author,
        'posts_count': posts_count,
    }
    context.update(get_page_context(post_list, request))
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    posts_count = author.posts.select_related('author').count()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    templates = "posts/post_create.html"
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    context = {
        'form': form
    }
    return render(request, templates, context)


@login_required
def post_edit(request, post_id):
    templates = "posts/post_create.html"
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post.pk)
    is_edit = True
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post.pk)
    context = {
        'form': form,
        'post': post,
        'is_edit': is_edit,
    }
    return render(request, templates, context)
