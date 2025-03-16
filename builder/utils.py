
from collections import Counter
from .models import MainGroup, Product  

def pc_list_is_completed(pc_list):
    """
    Check if PC list contains all required component types (main_group),
    and whether each type has exactly one product.
    """
    # 获取所有 MainGroup 主键
    all_main_groups = set(MainGroup.objects.values_list('mainGroup', flat=True))

    # 根据 pc_list (sku 列表) 获取所有 Product 实例
    products = Product.objects.filter(sku__in=pc_list)

    # 获取 products 中涉及到的 MainGroup 列表
    product_main_groups = [product.mainGroup.mainGroup for product in products]

    # 统计每个 MainGroup 出现次数
    main_group_counter = Counter(product_main_groups)

    # 1. 检查是否包含所有 MainGroup
    contains_all_groups = all_main_groups.issubset(main_group_counter.keys())

    # 2. 检查每个 MainGroup 是否只出现一次
    each_group_once = all(count == 1 for count in main_group_counter.values())

    # 返回最终判断
    return contains_all_groups and each_group_once






from .models import Product, ProductSpec

def product_is_compatible(product, pc_list):
    """
    检查 product 是否与 pc_list 里的所有产品兼容：
    - 如果 product 是 CPU，检查 pc_list 里是否已有主板，品牌和 socket 是否匹配；
    - 如果 product 是 主板，检查 pc_list 里是否已有 CPU，品牌和 socket 是否匹配。
    """

    pc_products = Product.objects.filter(sku__in=pc_list)

    # 判断 product 是 CPU 还是 主板
    product_group = product.mainGroup.mainGroupName

    # 如果是 CPU，去找主板
    if product_group == 'Processoren':
        for p in pc_products:
            if p.mainGroup.mainGroupName == 'Moederborden':
                # 比较品牌
                if product.brand != p.brand:
                    return False  # 品牌不同，不兼容
                # 比较 socket
                product_socket = ProductSpec.objects.filter(product=product, spec__spec='socket').first()
                board_socket = ProductSpec.objects.filter(product=p, spec__spec='socket').first()
                if product_socket and board_socket and product_socket.value.value != board_socket.value.value:
                    return False  # socket 不同，不兼容

    # 如果是 主板，去找 CPU
    elif product_group == 'Moederborden':
        for p in pc_products:
            if p.mainGroup.mainGroupName == 'Processoren':
                # 比较品牌
                if product.brand != p.brand:
                    return False  # 品牌不同，不兼容
                # 比较 socket
                product_socket = ProductSpec.objects.filter(product=product, spec__spec='socket').first()
                cpu_socket = ProductSpec.objects.filter(product=p, spec__spec='socket').first()
                if product_socket and cpu_socket and product_socket.value.value != cpu_socket.value.value:
                    return False  # socket 不同，不兼容

    return True  # 如果没有发现不兼容，则认为兼容

