from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from blogs.models import Category, Blog
from .forms import BlogForm


# ==========================
# Dashboard
# ==========================

@login_required(login_url='login')
def dashboard(request):

    context = {
        'category_count': Category.objects.count(),
        'blog_count': Blog.objects.count(),
    }

    return render(request, 'dashboard.html', context)


# ==========================
# Categories
# ==========================

@login_required(login_url='login')
def categories(request):

    categories = Category.objects.all().order_by('id')

    return render(request, 'categories.html', {
        'categories': categories
    })


# ==========================
# Add Category
# ==========================

@login_required(login_url='login')
def add_category(request):

    if request.method == "POST":

        category_name = request.POST.get("category_name")

        if not category_name:
            messages.error(request, "Category name is required.")
            return redirect("add_category")

        if Category.objects.filter(category_name__iexact=category_name).exists():
            messages.error(request, "Category already exists.")
            return redirect("add_category")

        Category.objects.create(category_name=category_name)

        messages.success(request, "Category added successfully.")
        return redirect("categories")

    return render(request, "add_category.html")


# ==========================
# Edit Category
# ==========================

@login_required(login_url='login')
def edit_category(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":

        category_name = request.POST.get("category_name")

        if not category_name:
            messages.error(request, "Category name is required.")
            return redirect("edit_category", pk=pk)

        if Category.objects.filter(
            category_name__iexact=category_name
        ).exclude(pk=pk).exists():

            messages.error(request, "Category already exists.")
            return redirect("edit_category", pk=pk)

        category.category_name = category_name
        category.save()

        messages.success(request, "Category updated successfully.")
        return redirect("categories")

    return render(request, "edit_category.html", {
        "category": category
    })


# ==========================
# Delete Category
# ==========================

@login_required(login_url='login')
def delete_category(request, pk):

    category = get_object_or_404(Category, pk=pk)

    category.delete()

    messages.success(request, "Category deleted successfully.")

    return redirect("categories")


# ==========================
# Posts
# ==========================

@login_required(login_url='login')
def posts(request):

    posts = Blog.objects.all().order_by("-created_at")

    return render(request, "posts.html", {
        "posts": posts
    })


# ==========================
# Add Post
# ==========================

@login_required(login_url='login')
def add_post(request):

    if request.method == "POST":

        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)

            # Logged in user becomes the author
            post.author = request.user

            post.save()

            messages.success(request, "Post added successfully.")

            return redirect("posts")

    else:

        form = BlogForm()

    return render(request, "add_post.html", {
        "form": form
    })
@login_required(login_url='login')
def edit_post(request, pk):

    post = get_object_or_404(Blog, pk=pk)

    if request.method == "POST":

        form = BlogForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

            messages.success(request, "Post updated successfully.")

            return redirect('posts')

    else:

        form = BlogForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'edit_post.html', context)

@login_required(login_url='login')
def delete_post(request, pk):

    post = get_object_or_404(Blog, pk=pk)

    if request.method == "POST":

        post.delete()

        messages.success(request, "Post deleted successfully.")

        return redirect("posts")

    return render(request, "delete_post.html", {
        "post": post
    })