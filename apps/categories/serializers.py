from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'sector', 'sector_display', 'description', 'image', 'is_active', 'metadata', 'created_at']
