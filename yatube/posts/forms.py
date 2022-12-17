from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        labels = {
            'text': 'Введите текст',
            'group': 'Выберите группу',
            'image': 'Вставьте картинки'
            }
        help_text = {
            'text': 'Текст вашего поста',
            'group': 'Пустая группа',
            'image': 'Вставьте картинки',
        }
