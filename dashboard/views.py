from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blogs.models import Category, Blog


@login_required(login_url='login')
def dashboard(request):
    context = {
        'category_count': Category.objects.count(),
        'blog_count': Blog.objects.count(),
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def categories(request):
    categories = Category.objects.all().order_by('id')

    return render(request, 'categories.html', {
        'categories': categories
    })


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


@login_required(login_url='login')
def edit_category(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":

        category_name = request.POST.get("category_name")

        if not category_name:
            messages.error(request, "Category name is required.")
            return redirect("edit_category", pk=pk)

        if Category.objects.filter(category_name__iexact=category_name).exclude(pk=pk).exists():
            messages.error(request, "Category already exists.")
            return redirect("edit_category", pk=pk)

        category.category_name = category_name
        category.save()

        messages.success(request, "Category updated successfully.")
        return redirect("categories")

    return render(request, "edit_category.html", {
        "category": category
    })
@login_required(login_url='login')
def delete_category(request, pk):

    category = get_object_or_404(Category, pk=pk)
    category.delete()

    messages.success(request, "Category deleted successfully.")

    return redirect('categories')