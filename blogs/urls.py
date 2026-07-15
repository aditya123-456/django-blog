from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.post_by_category, name='post_by_category'),
    path('blog/<slug:slug>/', views.blogs, name='blogs'),
]