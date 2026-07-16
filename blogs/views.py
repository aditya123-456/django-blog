from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Blog, Category, Comment


def post_by_category(request, category_id):

    category = get_object_or_404(Category, pk=category_id)

    posts = Blog.objects.filter(
        category=category,
        status='published'
    )

    categories = Category.objects.all()

    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'post_by_category.html', context)


def blogs(request, slug):

    single_blog = get_object_or_404(
        Blog,
        slug=slug,
        status='published'
    )

    # Save Comment
    if request.method == "POST":

        # Allow only logged in users to comment
        if not request.user.is_authenticated:
            return redirect('login')

        comment = request.POST.get('comment')

        if comment:
            Comment.objects.create(
                blog=single_blog,
                user=request.user,
                comment=comment
            )

        return redirect('blogs', slug=slug)

    comments = Comment.objects.filter(
        blog=single_blog
    ).order_by('-created_at')

    categories = Category.objects.all()

    context = {
        'single_blog': single_blog,
        'comments': comments,
        'categories': categories,
    }

    return render(request, 'blogs.html', context)


def search(request):

    keyword = request.GET.get('keyword')

    posts = Blog.objects.none()

    if keyword:
        posts = Blog.objects.filter(
            Q(title__icontains=keyword) |
            Q(short_description__icontains=keyword) |
            Q(blog_body__icontains=keyword),
            status='published'
        )

    categories = Category.objects.all()

    context = {
        'posts': posts,
        'keyword': keyword,
        'categories': categories,
    }

    return render(request, 'search.html', context)