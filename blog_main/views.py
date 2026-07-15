from django.shortcuts import render, redirect
from .forms import RegistrationForm
from blogs.models import Blog, Category
from assignments.models import About
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
import random


def home(request):
    categories = Category.objects.all()

    featured_posts = Blog.objects.filter(is_featured=True)
    featured_post = random.choice(list(featured_posts)) if featured_posts.exists() else None

    posts = Blog.objects.filter(
        status='published',
        is_featured=False
    ).order_by('-created_at')

    about = About.objects.first()

    context = {
        'categories': categories,
        'featured_posts': featured_posts,
        'featured_post': featured_post,
        'posts': posts,
        'about': about,
    }

    return render(request, 'home.html', context)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')