from django.forms import ModelForm
from . models import Post, PostComment
from django import forms


class PostForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        max_length=255,
        required=True,
    )

    tag = forms.CharField(
        label='タグ',
        max_length=200,
        required=True,
    )
    text = forms.CharField(
        label='説明文',
        widget=forms.Textarea,
        required=True,
    )


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = [
            'user_name',
            'message',
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs['value'] = '名無し'

