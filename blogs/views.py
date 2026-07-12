from django.shortcuts import render, get_object_or_404
from .models import Blog, Category

def post_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    posts = Blog.objects.filter(
        category=category,
        status='published'
    )

    context = {
        'category': category,
        'posts': posts,
    }

    return render(request, 'post_by_category.html', context)