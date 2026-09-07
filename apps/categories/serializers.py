from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'sector', 'sector_display', 'description',
            'image', 'is_active', 'metadata', 'created_at'
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


