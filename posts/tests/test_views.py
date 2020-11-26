from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from posts.models import Group, Post


class PageTest(TestCase):
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

    def setUp(self):
        super().setUp()
        self.authorized_client = Client()
        self.authorized_client.force_login(PageTest.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: name"
        templates_pages_names = {
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),
            'group.html': (
                reverse('group_list', kwargs={'slug': 'group_for_test'})
            ),
        }
        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template, template)

    def test_new_post_page_correct_context(self):
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_index_page_correct_context(self):
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(response.context.get('posts')[0].text,
                         PageTest.post.text)
        self.assertEqual(response.context.get('posts')[0].author,
                         PageTest.post.author)
        self.assertEqual(response.context.get('posts')[0].pub_date,
                         PageTest.post.pub_date)
        self.assertEqual(response.context.get('posts')[0].group,
                         PageTest.post.group)

    def test_group_page_correct_context(self):
        response = self.authorized_client.get(
            reverse('group_list',
                    kwargs={'slug': 'group_for_test'}))
        self.assertEqual(response.context.get('group').title,
                         PageTest.group.title)
        self.assertEqual(response.context.get('group').slug,
                         PageTest.group.slug)
        self.assertEqual(response.context.get('group').description,
                         PageTest.group.description)

# python3 manage.py test posts.tests.test_views.PageTest.test_new_post_page_correct_context
