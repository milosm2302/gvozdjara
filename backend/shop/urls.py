from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    current_user,
    CategoryViewSet,
    SubcategoryViewSet,
    ProductViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('subcategories', SubcategoryViewSet, basename='subcategory')
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('auth/user/', current_user, name='current_user'),
    path('', include(router.urls)),
]