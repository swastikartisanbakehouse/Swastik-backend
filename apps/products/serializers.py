from rest_framework import serializers
from .models import Product
from apps.categories.serializers import CategorySerializer
from apps.categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'category_id',
            'category_detail',
            'subcategory_name',
            'description',
            'price',
            'discount_price',
            'tax_percentage',
            'unit',
            'stock_quantity',
            'is_available',
            'is_active',
            'image',
            'brand',
            'tags',
            'attributes',
            'created_at'
        ]

    def get_image(self, obj):
        if not obj.image:
            return None
        image_str = str(obj.image)
        if image_str.startswith('http://') or image_str.startswith('https://'):
            return image_str
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_id'] = instance.category_id
        return representation


