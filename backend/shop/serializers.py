from rest_framework import serializers
from .models import (
    Category, Subcategory, Product, ProductVariant,
    ProductImage, Order, OrderItem
)


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


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order', 'created_at']


class ProductVariantSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'name', 'price_adjustment', 'final_price', 'sku',
            'in_stock', 'stock_quantity', 'created_at'
        ]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Nested relations
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'on_sale', 'sale_price',
            'category', 'category_name', 'subcategory', 'subcategory_name',
            'current_price', 'featured', 'in_stock', 'stock_quantity',
            'variants', 'images', 'created_at', 'updated_at'
        ]


# Serializers za Order i OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(read_only=True)
    variant_name = serializers.CharField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'variant', 'quantity',
            'unit_price', 'total_price',
            'product_name', 'variant_name'
        ]
        read_only_fields = ['unit_price', 'total_price', 'product_name', 'variant_name']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_phone', 'customer_email',
            'delivery_address', 'status', 'notes', 'admin_notes',
            'total_amount', 'created_at', 'updated_at',
            'sms_sent', 'email_sent', 'items'
        ]
        read_only_fields = ['total_amount', 'sms_sent', 'email_sent']


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer za kreiranje narudžbine sa stavkama
    """
    customer_name = serializers.CharField(max_length=200)
    customer_phone = serializers.CharField(max_length=20)
    customer_email = serializers.EmailField(required=False, allow_blank=True)
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    items = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )

    def validate_items(self, items):
        """Validacija stavki"""
        if not items:
            raise serializers.ValidationError("Narudžbina mora sadržati bar jednu stavku.")

        for item in items:
            if 'product_id' not in item:
                raise serializers.ValidationError("Nedostaje product_id u stavci.")
            if 'quantity' not in item or item['quantity'] < 1:
                raise serializers.ValidationError("Količina mora biti najmanje 1.")

        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # Kreiraj Order
        order = Order.objects.create(
            customer_name=validated_data['customer_name'],
            customer_phone=validated_data['customer_phone'],
            customer_email=validated_data.get('customer_email', ''),
            delivery_address=validated_data.get('delivery_address', ''),
            notes=validated_data.get('notes', ''),
            total_amount=0  # Temp, izračunaćemo ispod
        )

        total = 0

        # Kreiraj OrderItems
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            variant = None
            variant_name = ''

            if 'variant_id' in item_data and item_data['variant_id']:
                variant = ProductVariant.objects.get(id=item_data['variant_id'])
                unit_price = variant.final_price
                variant_name = variant.name
            else:
                unit_price = product.current_price

            quantity = item_data['quantity']
            total_price = unit_price * quantity
            total += total_price

            OrderItem.objects.create(
                order=order,
                product=product,
                variant=variant,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                product_name=product.name,
                variant_name=variant_name
            )

        # Update total
        order.total_amount = total
        order.save()

        return order