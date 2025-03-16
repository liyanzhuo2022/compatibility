from django.urls import path
from .views import finalize_pc_list, get_main_groups, get_pc_list, get_products_by_main_group, get_product_specs, add_to_pc_list, remove_from_pc_list
# this is the urls.py file for the apis

urlpatterns = [
    path('component-types/', get_main_groups, name='get_main_groups'),
    path('products/', get_products_by_main_group, name='get_products_by_main_group'),
    path('product/<int:sku>/specs/', get_product_specs, name='get_product_specs'),
    path('pc-list/', get_pc_list, name='get_pc_list'),
    path('pc-list/add/', add_to_pc_list, name='add_to_pc_list'),
    path('pc-list/remove/', remove_from_pc_list, name='remove_from_pc_list'),  
    path('pc-list/save/', finalize_pc_list, name='finalize_pc_list')
]
