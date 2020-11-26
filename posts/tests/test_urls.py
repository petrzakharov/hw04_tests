from django.test import TestCase, Client
from posts.models import Group
from django.contrib.auth import get_user_model


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
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

        cls.group = Group.objects.create(id=100,
                                         title='Группа для теста',
                                         slug='group_for_test',
                                         description='Группа для теста')

        cls.all_urls = {'authorized_user':
                            {'/': 200,
                             '/new/': 200,
                             '/group/group_for_test/': 200},
                        'anonymous_user': {'/': 200,
                                           '/new/': 302,
                                           '/group/group_for_test/': 200}
                        }
        cls.templates_url = {
            'index.html': '/',
            'group.html': '/group/group_for_test/',
            'new.html': '/new/'
        }

    def setUp(self):
        super().setUp()
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(NoStaticURLTests.user)

    def test_urls_response_for_anonymous_user(self):
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
