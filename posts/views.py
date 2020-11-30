from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get(
        "page")
    page = paginator.get_page(
        page_number)
    return render(
        request,
        "index.html",
        {"page": page, "paginator": paginator}
    )


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
    post = get_object_or_404(Post, id=post_id, author__username=username)
    return render(request, "post.html", {"post": post,
                                         "author": post.author})


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if post.author != request.user:
        return redirect("post", username, post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post", username, post_id)
    return render(request, "new.html", {"form": form,
                                        "is_edit": True,
                                        "post": post})
