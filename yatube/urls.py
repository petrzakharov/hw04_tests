from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.conf.urls import handler404, handler500
from posts import views as post_views

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

urlpatterns = [
    path("auth/", include("users.urls")),
    path('about/', include('django.contrib.flatpages.urls'), name='about'),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='spec'),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("posts.urls")),
    path("admin/", admin.site.urls)
]


