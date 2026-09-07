import json
from rest_framework import serializers
from .models import Product
from apps.categories.serializers import CategorySerializer
from apps.categories.models import Category

class HybridImageField(serializers.Field):
    """
    Flexible field that accepts string image URLs, image paths, file uploads, or null values.
    """
    def to_internal_value(self, data):
        if not data or data == 'null' or data == 'undefined':
            return None
        return data

    def to_representation(self, value):
        if not value:
            return None
        value_str = str(value)
        if value_str.startswith('http://') or value_str.startswith('https://'):
            return value_str
        request = self.context.get('request')
        if request and hasattr(value, 'url'):
            return request.build_absolute_uri(value.url)
        elif hasattr(value, 'url'):
            return value.url
        return value_str


class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    category_id = serializers.IntegerField(required=False, write_only=True)
    category = serializers.IntegerField(required=False, write_only=True)
    image = HybridImageField(required=False, allow_null=True)

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

    def to_internal_value(self, data):
        if hasattr(data, 'dict'):
            mutable_data = data.dict()
        elif isinstance(data, dict):
            mutable_data = data.copy()
        else:
            mutable_data = {}

        # 1. Normalize category / category_id input
        cat_val = mutable_data.get('category') if mutable_data.get('category') is not None else mutable_data.get('category_id')
        if isinstance(cat_val, dict):
            cat_val = cat_val.get('id') or cat_val.get('category_id')
        
        if cat_val is not None and cat_val != '' and cat_val != 'null':
            try:
                cat_id_int = int(cat_val)
                mutable_data['category'] = cat_id_int
                mutable_data['category_id'] = cat_id_int
            except (ValueError, TypeError):
                pass

        # 2. Normalize tags
        tags_val = mutable_data.get('tags')
        if isinstance(tags_val, str):
            tags_val = tags_val.strip()
            if tags_val.startswith('[') and tags_val.endswith(']'):
                try:
                    mutable_data['tags'] = json.loads(tags_val)
                except Exception:
                    mutable_data['tags'] = [t.strip() for t in tags_val.strip('[]').split(',') if t.strip()]
            elif ',' in tags_val:
                mutable_data['tags'] = [t.strip() for t in tags_val.split(',') if t.strip()]
            elif tags_val:
                mutable_data['tags'] = [tags_val]
            else:
                mutable_data['tags'] = []
        elif tags_val is None:
            mutable_data['tags'] = []

        # 3. Normalize attributes
        attr_val = mutable_data.get('attributes')
        if isinstance(attr_val, str):
            attr_val = attr_val.strip()
            if attr_val.startswith('{') and attr_val.endswith('}'):
                try:
                    mutable_data['attributes'] = json.loads(attr_val)
                except Exception:
                    mutable_data['attributes'] = {}
            else:
                mutable_data['attributes'] = {}
        elif attr_val is None:
            mutable_data['attributes'] = {}

        # 4. Normalize discount_price
        disc_price = mutable_data.get('discount_price')
        if disc_price == '' or disc_price == 'null' or disc_price is None:
            mutable_data['discount_price'] = None

        # 5. Normalize booleans
        for bool_field in ['is_active', 'is_available']:
            if bool_field in mutable_data:
                val = mutable_data[bool_field]
                if isinstance(val, str):
                    mutable_data[bool_field] = val.lower() in ('true', '1', 't', 'yes')

        return super().to_internal_value(mutable_data)

    def validate(self, attrs):
        # Resolve category ForeignKey object from category / category_id int
        cat_id = attrs.pop('category_id', None)
        category_input = attrs.pop('category', None)
        target_cat_id = category_input if category_input is not None else cat_id

        if target_cat_id is not None:
            try:
                attrs['category'] = Category.objects.get(pk=target_cat_id)
            except (Category.DoesNotExist, ValueError, TypeError):
                raise serializers.ValidationError({
                    'category': f'Category with ID {target_cat_id} does not exist.'
                })

        if 'category' not in attrs and not self.partial:
            raise serializers.ValidationError({'category': 'Category ID is required.'})

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_id'] = instance.category_id
        return representation




