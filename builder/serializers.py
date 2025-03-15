from rest_framework import serializers
from .models import Product

# Product serializer (restructured to use mainGroup instead of componentType)
class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.brandName')
    mainGroup = serializers.CharField(source='mainGroup.mainGroupName')  # Now showing component type via mainGroup

    class Meta:
        model = Product
        fields = ['sku', 'productName', 'brand', 'mainGroup']  # Return mainGroup instead of componentType
