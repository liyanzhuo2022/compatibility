from django.urls import path
from .views import get_main_groups, get_products_by_main_group, get_product_specs

urlpatterns = [
    path('component-types/', get_main_groups, name='get_main_groups'),
    path('products/', get_products_by_main_group, name='get_products_by_main_group'),
    path('product/<int:sku>/specs/', get_product_specs, name='get_product_specs'),
]
