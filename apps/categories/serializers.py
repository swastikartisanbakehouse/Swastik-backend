from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    image = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'sector', 'sector_display', 'description',
            'image', 'is_active', 'metadata', 'created_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
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



