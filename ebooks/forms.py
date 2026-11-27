from django import forms
from .models import Ebook, Chapter


class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['title', 'subtitle', 'author', 'template_style', 'cover_artwork']


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['order', 'title', 'content']
