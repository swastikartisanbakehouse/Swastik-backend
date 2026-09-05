from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

# Customer Category Views
class CategoryListView(generics.ListAPIView):
    """
    GET /api/categories
    Returns list of active categories.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class CategoryDetailView(generics.RetrieveAPIView):
    """
    GET /api/categories/:id
    Returns details of a specific active category.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# Admin Category Views
class AdminCategoryListCreateView(generics.ListCreateAPIView):
    """
    GET /api/admin/categories (List all categories including inactive)
    POST /api/admin/categories (Create a new category)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/admin/categories/:id
    PUT /api/admin/categories/:id
    PATCH /api/admin/categories/:id
    DELETE /api/admin/categories/:id
    Updates or deletes a category (Admin only).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

