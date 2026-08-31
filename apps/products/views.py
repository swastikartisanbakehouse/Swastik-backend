from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer

# Customer Product Views
class ProductListView(generics.ListAPIView):
    """
    GET /api/products
    Supports query parameters:
    - ?category_id=<id>
    - ?sector=BAKERY | DAIRY | SWEETS | CONFECTIONERY
    - ?sku=<sku>
    - ?in_stock=true | false
    - ?subcategory=<name>
    - ?search=<keyword>
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        category_id = self.request.query_params.get('category_id')
        sector = self.request.query_params.get('sector')
        sku = self.request.query_params.get('sku')
        in_stock = self.request.query_params.get('in_stock')
        subcategory = self.request.query_params.get('subcategory')
        search_query = self.request.query_params.get('search')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if sector:
            queryset = queryset.filter(category__sector__iexact=sector)

        if sku:
            queryset = queryset.filter(sku__iexact=sku)

        if in_stock is not None:
            if in_stock.lower() == 'true':
                queryset = queryset.filter(is_available=True, stock_quantity__gt=0)
            elif in_stock.lower() == 'false':
                queryset = queryset.filter(Q(is_available=False) | Q(stock_quantity=0))

        if subcategory:
            queryset = queryset.filter(subcategory_name__icontains=subcategory)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(sku__icontains=search_query) |
                Q(brand__icontains=search_query) |
                Q(subcategory_name__icontains=search_query)
            )

        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    """
    GET /api/products/:id
    """
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class CategoryProductListView(generics.ListAPIView):
    """
    GET /api/categories/:id/products
    List active products belonging to a specific category.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id, is_active=True).select_related('category')


# Admin Product Views
class AdminProductListCreateView(generics.ListCreateAPIView):
    """
    GET /api/admin/products (List all products including inactive)
    POST /api/admin/products (Create new product entry)
    """
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/admin/products/:id
    PATCH /api/admin/products/:id
    DELETE /api/admin/products/:id
    """
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
