from django.shortcuts import render
from blogs.models import Category, Blog
import random

def home(request):
    categories = Category.objects.all()

    featured_posts = Blog.objects.filter(is_featured=True)
    featured_post = random.choice(list(featured_posts)) if featured_posts.exists() else None

    posts = Blog.objects.filter(status='published', is_featured=False).order_by('-created_at')

    context = {
        'categories': categories,
        'featured_posts': featured_posts,
        'featured_post': featured_post,
        'posts': posts,
    }

    return render(request, 'home.html', context)