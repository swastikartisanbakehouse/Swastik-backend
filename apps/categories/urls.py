from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    AdminCategoryCreateView,
    AdminCategoryUpdateDeleteView,
)

urlpatterns = [
    # Customer APIs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Admin APIs
    path('admin/categories/', AdminCategoryCreateView.as_view(), name='admin-category-create'),
    path('admin/categories/<int:pk>/', AdminCategoryUpdateDeleteView.as_view(), name='admin-category-detail'),
]
