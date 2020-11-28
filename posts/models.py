from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextField

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text: TextField = models.TextField(verbose_name="Текст поста",
                                       help_text="Поле для ввода текста поста")
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(
        "Group", related_name="posts", blank=True,
        null=True, on_delete=models.SET_NULL, verbose_name="Группа",
        help_text="Поле для ввода группы публикции")

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:15]
