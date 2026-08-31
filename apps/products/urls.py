from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    CategoryProductListView,
    AdminProductListCreateView,
    AdminProductDetailUpdateDeleteView,
)

urlpatterns = [
    # Customer APIs
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/<int:category_id>/products/', CategoryProductListView.as_view(), name='category-products'),

    # Admin APIs
    path('admin/products/', AdminProductListCreateView.as_view(), name='admin-product-list-create'),
    path('admin/products/<int:pk>/', AdminProductDetailUpdateDeleteView.as_view(), name='admin-product-detail'),
]
