from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("group", "text")
        labels = {"text": "Текст поста", "group": "Группа поста"}
        help_texts = {"text": "Напишите ваш пост здесь",
                      "group": "Укажите в какую группу опубликовать пост"}
