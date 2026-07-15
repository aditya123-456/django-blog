from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Blog, Category


def post_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    posts = Blog.objects.filter(
        category=category,
        status='published'
    )

    return render(request, 'post_by_category.html', {
        'category': category,
        'posts': posts,
    })


def blogs(request, slug):
    single_blog = get_object_or_404(
        Blog,
        slug=slug,
        status='published'
    )

    return render(request, 'blogs.html', {
        'single_blog': single_blog,
    })


def search(request):
    keyword = request.GET.get('keyword', '')

    posts = Blog.objects.none()

    if keyword:
        posts = Blog.objects.filter(
            Q(title__icontains=keyword) |
            Q(short_description__icontains=keyword) |
            Q(blog_body__icontains=keyword),
            status='published'
        )

    return render(request, 'search.html', {
        'posts': posts,
        'keyword': keyword,
    })