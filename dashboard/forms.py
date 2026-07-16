from django import forms
from blogs.models import Blog


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog

        fields = [
            'title',
            'category',
            'featured_image',
            'short_description',
            'blog_body',
            'status',
            'is_featured',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'slug': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'blog_body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),

            'featured_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }