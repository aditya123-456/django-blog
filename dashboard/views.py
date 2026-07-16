from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from functools import wraps
from django.http import HttpResponseForbidden

from blogs.models import Category, Blog
from .forms import BlogForm, UserRegisterForm, UserEditForm
# ======================================
# Manager Permission
# ======================================

def manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # Superuser has full access
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # User belongs to Manager group
        if request.user.groups.filter(name="Manager").exists():
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden(
            "You are not authorized to access this page."
        )

    return wrapper


# ======================================
# Dashboard
# ======================================

@login_required(login_url='login')
@manager_required
def dashboard(request):

    context = {
        'category_count': Category.objects.count(),
        'blog_count': Blog.objects.count(),
        'user_count': User.objects.count(),
    }

    return render(request, 'dashboard.html', context)


# ======================================
# Users
# ======================================

@login_required(login_url='login')
@manager_required
def users(request):

    users = User.objects.all().order_by('id')

    return render(request, 'users.html', {
        'users': users
    })


# ======================================
# Add User
# ======================================

@login_required(login_url='login')
@manager_required
def add_user(request):
    if request.method == "POST":

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "User added successfully.")

            return redirect('users')

    else:

        form = UserRegisterForm()

    return render(request, 'add_user.html', {
        'form': form
    })


# ======================================
# Edit User
# ======================================

@login_required(login_url='login')
@manager_required
def edit_user(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        form = UserEditForm(request.POST, instance=user)

        if form.is_valid():

            form.save()

            messages.success(request, "User updated successfully.")

            return redirect("users")

    else:

        form = UserEditForm(instance=user)

    return render(request, "edit_user.html", {
        "form": form,
        "user": user
    })
# ======================================
# Delete User
# ======================================

@login_required(login_url='login')
@manager_required
def delete_user(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        user.delete()

        messages.success(request, "User deleted successfully.")

        return redirect('users')

    return render(request, 'delete_user.html', {
        'user': user
    })


# ======================================
# Categories
# ======================================

@login_required(login_url='login')
@manager_required
def categories(request):

    categories = Category.objects.all().order_by('id')

    return render(request, 'categories.html', {
        'categories': categories
    })


# ======================================
# Add Category
# ======================================

@login_required(login_url='login')
@manager_required
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


# ======================================
# Edit Category
# ======================================

@login_required(login_url='login')
@manager_required
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


# ======================================
# Delete Category
# ======================================

@login_required(login_url='login')
@manager_required
def delete_category(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":

        category.delete()

        messages.success(request, "Category deleted successfully.")

        return redirect("categories")

    return render(request, "delete_category.html", {
        "category": category
    })


# ======================================
# Posts
# ======================================

@login_required(login_url='login')
@manager_required
def posts(request):

    posts = Blog.objects.all().order_by('-created_at')

    return render(request, 'posts.html', {
        'posts': posts
    })


# ======================================
# Add Post
# ======================================

@login_required(login_url='login')
@manager_required
def add_post(request):

    if request.method == "POST":

        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            post.save()

            messages.success(request, "Post added successfully.")

            return redirect("posts")

    else:

        form = BlogForm()

    return render(request, "add_post.html", {
        "form": form
    })


# ======================================
# Edit Post
# ======================================

@login_required(login_url='login')
@manager_required
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

            return redirect("posts")

    else:

        form = BlogForm(instance=post)

    return render(request, "edit_post.html", {
        "form": form,
        "post": post
    })


# ======================================
# Delete Post
# ======================================

@login_required(login_url='login')
@manager_required
def delete_post(request, pk):

    post = get_object_or_404(Blog, pk=pk)

    if request.method == "POST":

        post.delete()

        messages.success(request, "Post deleted successfully.")

        return redirect("posts")

    return render(request, "delete_post.html", {
        "post": post
    })