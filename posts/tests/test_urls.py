from django.test import TestCase, Client
from posts.models import Group, Post
from django.contrib.auth import get_user_model
from django.urls import reverse


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        """
        Тестирование страницы Об авторе
        """
        response = self.guest_client.get('/about-author/')
        self.assertEqual(response.status_code, 200)

    def test_tech(self):
        """
        Тестирование страницы Технологии
        """
        response = self.guest_client.get('/about-spec/')
        self.assertEqual(response.status_code, 200)


class NoStaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username='TestUser')
        cls.user_without_posts = \
            get_user_model().objects.create_user(username='user_without_posts')

        cls.group = Group.objects.create(id=100,
                                         title='Группа для теста',
                                         slug='group_for_test',
                                         description='Группа для теста')
        cls.post = Post.objects.create(id=100,
                                       text='Test post',
                                       author=cls.user)

        cls.all_urls = \
            dict(authorized_user={reverse('index'): 200,
                                  reverse('new_post'): 200,
                                  reverse('group_list',
                                          kwargs={
                                              'slug': 'group_for_test'}
                                          ): 200,
                                  reverse('profile',
                                          kwargs={
                                              'username': 'TestUser'}
                                          ): 200,
                                  reverse('post',
                                          kwargs={
                                              'username': 'TestUser',
                                              'post_id': 100}
                                          ): 200,
                                  reverse('post_edit',
                                          kwargs={
                                              'username': 'TestUser',
                                              'post_id': 100}
                                          ): 200,
                                  reverse('post_edit',
                                          kwargs={
                                              'username': 'user_without_posts',
                                              'post_id': 100}
                                          ): 404,

                                  },
                 anonymous_user={
                reverse('new_post'): 302,
                reverse('post_edit',
                        kwargs={'username': 'TestUser',
                                'post_id': 100}
                        ): 302
            })
        cls.templates_url = {
            'index.html': reverse('index'),
            'group.html': reverse('group_list',
                                  kwargs={'slug': 'group_for_test'}
                                  ),
            'new.html': reverse('new_post'),
            'new.html': reverse('post_edit',
                                  kwargs={'username': 'TestUser',
                                          'post_id': 100}
                                  )

        }

    def setUp(self):
        super().setUp()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(NoStaticURLTests.user)

    def test_urls_response_anonymous_user(self):
        for url, code in (NoStaticURLTests.all_urls['anonymous_user']).items():
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, code, url)

    def test_urls_response_authorized_user(self):
        for url, code in \
                (NoStaticURLTests.all_urls['authorized_user']).items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, code, url)

    def test_urls_uses_correct_template(self):
        for template, url in NoStaticURLTests.templates_url.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template, url)


    #дописать здесь тестирование редиректов (посмотреть как правильно)
    #Отдельно написать функцию для тестирования редактирования поста от другого юзера
        #авторизовать клиент под юзером без постов

    #дописать тестирование flatpages (посмотреть как правильно в слаке)
    #вынести большие словари в глобальные переменные в самое начало файла,
        #чтобы код смотрелся красивее

    #написать докстринги