from rest_framework import serializers
from .models import Category, Subcategory, Product

from rest_framework import serializers
from .models import Category, Subcategory, Product


class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'description', 'category', 'category_name', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    product_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'subcategories', 'product_count', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'on_sale', 'sale_price',
            'category', 'category_name', 'subcategory', 'subcategory_name',
            'current_price', 'created_at', 'updated_at'
        ]