from rest_framework import serializers
from .models import Product
from apps.categories.serializers import CategorySerializer
from apps.categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        required=False,
        write_only=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        write_only=True
    )
    image = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'category',
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

    def validate(self, attrs):
        category = attrs.get('category')
        if not category and 'category_id' in self.initial_data:
            cat_id = self.initial_data.get('category_id')
            try:
                attrs['category'] = Category.objects.get(pk=cat_id)
            except (Category.DoesNotExist, ValueError, TypeError):
                raise serializers.ValidationError({'category_id': f'Invalid category ID: {cat_id}'})

        if not attrs.get('category') and not self.partial:
            raise serializers.ValidationError({'category': 'This field is required.'})
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_id'] = instance.category_id

        if instance.image:
            image_str = str(instance.image)
            if image_str.startswith('http://') or image_str.startswith('https://'):
                representation['image'] = image_str
            else:
                request = self.context.get('request')
                if request:
                    representation['image'] = request.build_absolute_uri(instance.image.url)
                else:
                    representation['image'] = instance.image.url
        else:
            representation['image'] = None

        return representation



