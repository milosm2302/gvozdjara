from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import (
    Category, Subcategory, Product, ProductVariant,
    ProductImage, Order, OrderItem
)
from .serializers import (
    CategorySerializer, SubcategorySerializer, ProductSerializer,
    ProductVariantSerializer, ProductImageSerializer,
    OrderSerializer, OrderCreateSerializer
)


# User info endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
    })


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUser()]


# Subcategory ViewSet
class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUser()]


# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUser()]


# ProductVariant ViewSet
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = ProductVariant.objects.all()
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset


# ProductImage ViewSet
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = ProductImage.objects.all()
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        # Samo admini mogu videti sve narudžbine
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        # CREATE je javno dostupan (korisnici kreiraju narudžbine)
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Pošalji email notifikaciju vlasniku
        self.send_order_notification(order)

        # TODO: Pošalji SMS korisniku i vlasniku (implementirati kasnije)

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

    def send_order_notification(self, order):
        """Pošalji email notifikaciju vlasniku o novoj narudžbini"""
        try:
            subject = f'Nova narudžbina #{order.id}'
            message = f"""
Nova narudžbina je primljena!

Narudžbina: #{order.id}
Kupac: {order.customer_name}
Telefon: {order.customer_phone}
Email: {order.customer_email or 'Nije ostavljen'}
Ukupno: {order.total_amount} RSD

Stavke:
"""
            for item in order.items.all():
                variant_info = f" ({item.variant_name})" if item.variant_name else ""
                message += f"- {item.product_name}{variant_info} x{item.quantity} = {item.total_price} RSD\n"

            if order.notes:
                message += f"\nNapomena kupca: {order.notes}"

            # Email za vlasnike
            recipient_list = ['office@betapack.co.rs']  # TODO: prebaciti u settings

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=True,
            )

            order.email_sent = True
            order.save(update_fields=['email_sent'])

        except Exception as e:
            print(f"Email send error: {e}")

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        """Ažuriraj status narudžbine"""
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response({'status': 'success', 'new_status': order.status})

        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )