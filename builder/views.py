from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MainGroup, Product, ProductSpec
from .serializers import ProductSerializer
from rest_framework import status
from .utils import pc_list_is_completed, product_is_compatible
from rest_framework.pagination import PageNumberPagination

# 自定义分页类（也可以直接用 DRF 内置的 PageNumberPagination）
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # 每页显示 10 个产品
    page_size_query_param = 'page_size'  # 允许前端通过 ?page_size=xx 调整每页数量
    max_page_size = 100  # 最多显示 100 个

# 1. Get all component types (actually MainGroup)
@api_view(['GET'])
def get_main_groups(request):
    """
    API endpoint to get all component categories (MainGroup).
    :param request: HTTP request
    :return: JSON list of component categories
    """
    try:
        main_groups = MainGroup.objects.all()
        data = [{"id": mg.mainGroup, "name": mg.mainGroupName} for mg in main_groups]
        return Response(data, status=200)
    except Exception as e:
        return Response({"error": "Internal Server Error", "message": "Cannot get component categories."}, status=500)


# 2. Get products by MainGroup (component type)
@api_view(['GET'])
def get_products_by_main_group(request):
    """
    API endpoint to get all products of a specific component type (MainGroup) with pagination.
    :param request: HTTP request
    :return: Paginated JSON list of products
    """
    # Get URL parameter ?type=CPU
    group_name = request.GET.get('type')

    # Check if 'type' parameter is provided
    if not group_name:
        return Response({"error": "Parameter 'type' is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if MainGroup (component type) exists
    try:
        main_group = MainGroup.objects.get(mainGroupName=group_name)
    except MainGroup.DoesNotExist:
        return Response({"error": f"Component type '{group_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Filter products belonging to this component type
    products = Product.objects.filter(mainGroup=main_group)

    # 分页器
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(products, request)

    # 序列化分页后的数据
    serializer = ProductSerializer(result_page, many=True)

    # 返回分页响应
    return paginator.get_paginated_response({
        "type": group_name,  # Return the queried component type
        "products": serializer.data
    })

# 3. Get product specs by SKU
@api_view(['GET'])
def get_product_specs(request, sku):
    """
    API endpoint to get all specifications of a specific product.
    :param request: HTTP request
    :param sku: Product SKU from URL
    :return: JSON response with all specs or error message
    """
    try:
        # Check if product exists
        product = Product.objects.get(sku=sku)
    except Product.DoesNotExist:
        return Response({
            "error": "Not Found",
            "message": "Specifications for this product cannot be found."
        }, status=status.HTTP_404_NOT_FOUND)

    # Get all specs associated with this product
    product_specs = ProductSpec.objects.filter(product=product)

    # Build specs dictionary
    specs_dict = {}
    for ps in product_specs:
        specs_dict[ps.spec.spec] = ps.value.value  # spec name : spec value

    return Response({
        "specs": specs_dict
    }, status=status.HTTP_200_OK)

# 4. get pclist
@api_view(['GET'])
def get_pc_list(request):
    """
    API to retrieve the current PC List stored in session.
    """
    pc_list = request.session.get('pc_list', [])
    products = Product.objects.filter(sku__in=pc_list)

    # 序列化产品数据返回
    serializer = ProductSerializer(products, many=True)

    return Response({"pc_list": serializer.data})

# 5. add product to pclist
@api_view(['POST'])
def add_to_pc_list(request):
    """
    API to add a product to PC List, with compatibility check (placeholder now).
    """

    sku = request.data.get('sku')

    if not sku:
        return Response({
            "success": False,
            "message": "No SKU provided."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(sku=sku)
    except Product.DoesNotExist:
        return Response({
            "success": False,
            "message": f"Product with SKU {sku} does not exist."
        }, status=status.HTTP_404_NOT_FOUND)

    pc_list = request.session.get('pc_list', [])
    current_products = Product.objects.filter(sku__in=pc_list)

    # 兼容性检查（调用占位函数，先 always True）
    if not product_is_compatible(product, current_products):
        return Response({
            "success": False,
            "message": f"Product {product.productName} is not compatible with current PC List."
        }, status=status.HTTP_400_BAD_REQUEST)

    # 添加产品到 PC List（避免重复）
    if sku not in pc_list:
        pc_list.append(sku)
        request.session['pc_list'] = pc_list  # 存回 session

    return Response({
        "success": True,
        "message": f"Product {product.productName} added to PC List."
    }, status=status.HTTP_200_OK)

# 6. remove product from pclist
@api_view(['POST'])
def remove_from_pc_list(request):
    """
    API to remove a product from PC List.
    """
    sku = request.data.get('sku')

    # 检查是否提供 SKU
    if not sku:
        return Response({
            "success": False,
            "message": "No SKU provided."
        }, status=status.HTTP_400_BAD_REQUEST)

    # 获取当前 PC List
    pc_list = request.session.get('pc_list', [])

    # 检查 SKU 是否在 PC List 中
    if sku not in pc_list:
        return Response({
            "success": False,
            "message": f"Product with SKU {sku} is not in PC List."
        }, status=status.HTTP_404_NOT_FOUND)

    # 移除产品
    pc_list.remove(sku)
    request.session['pc_list'] = pc_list  # 更新 session

    return Response({
        "success": True,
        "message": f"Product with SKU {sku} has been removed from PC List."
    }, status=status.HTTP_200_OK)

# 7. save pclist
@api_view(['POST'])
def finalize_pc_list(request):
    """
    Finalize the PC List for the user to copy/save.
    complete check is a placeholder now.
    """
    pc_list = request.session.get('pc_list', [])

    if not pc_list:
        return Response({
            "success": False,
            "message": "Your PC List is empty. Nothing to export."
        }, status=status.HTTP_400_BAD_REQUEST)

    # 查询产品详情
    products = Product.objects.filter(sku__in=pc_list)

    # 完整性检查
    if not pc_list_is_completed(products):
        return Response({
            "success": False,
            "message": "Your PC List is incomplete. Please ensure all required components are selected."
        }, status=status.HTTP_400_BAD_REQUEST)

    # 构建结果
    result = []
    for p in products:
        result.append({
            "sku": p.sku,
            "productName": p.productName,
            "brand": p.brand.brandName,
            "mainGroup": p.mainGroup.mainGroupName
        })

    return Response({
        "success": True,
        "message": "Your PC build is complete and ready!",
        "pc_list": result,
    }, status=status.HTTP_200_OK)


# for pages
def home(request):
    return render(request, 'home.html')

def components(request):
    return render(request, 'components.html')

def product_detail(request):
    return render(request, 'product_detail.html')

def pc_list(request):
    return render(request, 'pc_list.html')


