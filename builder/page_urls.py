from django.urls import path
from .views import home ,components, product_detail, pc_list

urlpatterns = [
    path('', home, name='home'),  # 首页
    path('components/', components, name='components'), 
    path('pc-list/', pc_list, name='pc_list'),  
    path('product-detail/', product_detail, name='product_detail'),  
]
