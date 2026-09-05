from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    AdminCategoryListCreateView,
    AdminCategoryDetailView,
)

urlpatterns = [
    # Customer APIs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Admin APIs
    path('admin/categories/', AdminCategoryListCreateView.as_view(), name='admin-category-list-create'),
    path('admin/categories/<int:pk>/', AdminCategoryDetailView.as_view(), name='admin-category-detail'),
]

