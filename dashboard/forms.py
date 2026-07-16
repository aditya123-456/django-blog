from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm
from blogs.models import Blog


# ==========================
# Blog Form
# ==========================

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

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'featured_image': forms.ClearableFileInput(attrs={
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

            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# ==========================
# User Registration Form
# ==========================

class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    is_active = forms.BooleanField(
        required=False
    )

    is_staff = forms.BooleanField(
        required=False
    )

    is_superuser = forms.BooleanField(
        required=False
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control'
        })
    )

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:

        model = User

        fields = [

            'username',

            'first_name',

            'last_name',

            'email',

            'is_active',

            'is_staff',

            'is_superuser',

            'groups',

            'user_permissions',

            'password1',

            'password2',
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        user.is_active = self.cleaned_data['is_active']
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']

        if commit:
            user.save()

            user.groups.set(self.cleaned_data['groups'])

            user.user_permissions.set(
                self.cleaned_data['user_permissions']
            )

        return user
# ==========================
# User Edit Form
# ==========================

class UserEditForm(forms.ModelForm):

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control'
        })
    )

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control'
        })
    )

    class Meta:

        model = User

        fields = [

            'username',

            'first_name',

            'last_name',

            'email',

            'is_active',

            'is_staff',

            'is_superuser',

            'groups',

            'user_permissions',

        ]

        widgets = {

            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

        }