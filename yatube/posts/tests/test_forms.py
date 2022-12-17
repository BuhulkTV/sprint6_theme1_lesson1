from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )
        cls.post_group = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост с группой',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.user)

    def test_post_create_with_group(self):
        """Валидная форма создает запись Post с группой"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'auth'}
        ))
        post_response = Post.objects.latest('pub_date')
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post_response.text, form_data['text'])
        self.assertEqual(post_response.group.pk, form_data['group'])

    def test_post_edit_with_group(self):
        """После редактирования Post с группой изменяется в БД"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тест редактирования поста',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post_group.pk}),
            data=form_data,
            follow=True,
        )
        post_response = Post.objects.latest('pub_date')
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': post_response.pk}
        ))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(post_response.text, form_data['text'])
        self.assertEqual(post_response.group.pk, form_data['group'])
