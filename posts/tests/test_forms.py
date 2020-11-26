from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.forms import PostForm
from django.urls import reverse
from django import forms
from posts.models import Group, Post


"""
1. Проверка, что создается запись, проверить количество записей
2. Переадресация формы
3. Переопределенный help texts и лейблы

"""

class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username='TestUser')

        cls.group = Group.objects.create(id=100,
                                         title='Группа для теста',
                                         slug='group_for_test',
                                         description='Группа для теста')

        cls.post = Post.objects.create(text='Информативный тестовый пост',
                                       author=cls.user,
                                       group=Group.objects.get(id=100))

        cls.form = PostForm()

    def setUp(self):
        super().setUp()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTest.user)

    def test_group_label(self):
        group_label = PostFormTest.form.fields['group'].label
        self.assertEqual(group_label, 'Группа поста')

    def test_text_label(self):
        text_label = PostFormTest.form.fields['text'].label
        self.assertEqual(text_label, 'Текст поста')

    def test_group_help_text(self):
        group_help_text = PostFormTest.form.fields['group'].help_text
        self.assertEqual(group_help_text,
                         'Укажите в какую группу опубликовать пост')

    def test_text_help_text(self):
        text_help_text = PostFormTest.form.fields['text'].help_text
        self.assertEqual(text_help_text,
                         'Напишите ваш пост здесь')

    def test_create_post_in_group(self):
        form_data = {
            'group': PostFormTest.group.id,
            'text': 'Тестовый текст'
        }
        posts_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, '/')
        self.assertEqual(Post.objects.count(), posts_count + 1)

