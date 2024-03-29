from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username="TestUser")

        cls.group = Group.objects.create(title="Группа для теста",
                                         slug="group_for_test",
                                         description="Группа для теста")

        cls.post = Post.objects.create(text="Информативный тестовый пост",
                                       author=cls.user,
                                       group=cls.group)

        cls.form = PostForm()

    def setUp(self):
        super().setUp()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTest.user)

    def test_group_label(self):
        group_label = PostFormTest.form.fields["group"].label
        self.assertEqual(group_label, "Группа поста")

    def test_text_label(self):
        text_label = PostFormTest.form.fields["text"].label
        self.assertEqual(text_label, "Текст поста")

    def test_group_help_text(self):
        group_help_text = PostFormTest.form.fields["group"].help_text
        self.assertEqual(group_help_text,
                         "Укажите в какую группу опубликовать пост")

    def test_text_help_text(self):
        text_help_text = PostFormTest.form.fields["text"].help_text
        self.assertEqual(text_help_text,
                         "Напишите ваш пост здесь")

    def test_create_post_in_group(self):
        form_data = {
            "group": PostFormTest.group.id,
            "text": "Тестовый текст"
        }
        posts_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse("new_post"),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post_in_group(self):
        form_data = {
            "group": PostFormTest.post.group,
            "text": PostFormTest.post.text + "_updated!"
        }
        self.authorized_client.post(
            reverse("post_edit", kwargs={"username":
                                         PostFormTest.user.username,
                                         "post_id": PostFormTest.post.id}),
            data=form_data, follow=True)
        self.assertEqual(form_data["text"],
                         PostFormTest.post.text + "_updated!")
