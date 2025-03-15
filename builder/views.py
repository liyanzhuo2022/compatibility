from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MainGroup, Product, ProductSpec
from .serializers import ProductSerializer
from rest_framework import status
from .utils import pc_list_is_completed, product_is_compatible



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
    API endpoint to get all products of a specific component type (MainGroup).
    :param request: HTTP request
    :return: JSON list of products
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

    # Serialize and return the response
    serializer = ProductSerializer(products, many=True)

    return Response({
        "type": group_name,  # Return the queried component type
        "products": serializer.data
    }, status=status.HTTP_200_OK)


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
