from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User

# def index(request):
#     latest = Post.objects.all()[:11]
#     return render(request, "index.html", {"posts": latest})


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)  # показывать 10 записей на странице.
    page_number = request.GET.get(
        "page")  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(
        page_number)  # получить записи с нужным смещением
    return render(
        request,
        "index.html",
        {"page": page, "paginator": paginator}
    )


# def group_posts(request, slug):
#     group = get_object_or_404(Group, slug=slug)
#     posts = group.posts.all()[:12]
#     return render(request, "group.html", {"group": group, "posts": posts})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group,
                                          "page": page,
                                          "paginator": paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form_instance_updated = form.save(commit=False)
        form_instance_updated.author = request.user
        form_instance_updated.save()
        return redirect("index")
    return render(request, "new.html", {"form": form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = user.posts.all()
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"user_profile": user,
                                            "page": page,
                                            "paginator": paginator})


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(user.posts, pk=post_id)
    return render(request, "post.html", {"post": post,
                                         "author": user})


def post_edit(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(user.posts, pk=post_id)
    if post.author != request.user:
        return redirect("post", username, post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post", username, post_id)
    return render(request, "new.html", {"form": form,
                                        "is_edit": True,
                                        "post": post})
