from .models import Product, ProductSpec


def check_pair_compatibility(product1, product2):
    """
    一对一配对检查：如 CPU-主板 插槽匹配，内存类型匹配，GPU-电源功率检查等。
    """

    mg1 = product1.mainGroup.mainGroupName
    mg2 = product2.mainGroup.mainGroupName

    # === CPU 和 主板 插槽 socket 检查 ===
    if {mg1, mg2} == {'Processoren', 'Moederborden'}:
        socket1 = ProductSpec.objects.filter(product=product1, spec__spec='socket').first()
        socket2 = ProductSpec.objects.filter(product=product2, spec__spec='socket').first()
        if socket1 and socket2 and socket1.value.value != socket2.value.value:
            return False, f"Incompatible socket: {socket1.value.value} vs {socket2.value.value}"

    # === 内存 和 主板 内存类型检查 ===
    if {mg1, mg2} == {'Geheugen', 'Moederborden'}:
        ram_type1 = ProductSpec.objects.filter(product=product1, spec__spec='ram_type').first()
        ram_type2 = ProductSpec.objects.filter(product=product2, spec__spec='ram_type').first()
        if ram_type1 and ram_type2 and ram_type1.value.value != ram_type2.value.value:
            return False, f"Incompatible RAM type: {ram_type1.value.value} vs {ram_type2.value.value}"

    # === GPU 和 电源 功率检查 ===
    if {mg1, mg2} == {'Videokaarten', 'Voedingen'}:
        gpu_power = ProductSpec.objects.filter(product=product1, spec__spec='power').first()
        psu_watt = ProductSpec.objects.filter(product=product2, spec__spec='watt').first()
        if not gpu_power or not psu_watt:
            return True, None  # 无法检查就不报错
        if int(psu_watt.value.value) < int(gpu_power.value.value):
            return False, f"PSU wattage too low for GPU: {psu_watt.value.value}W < {gpu_power.value.value}W"

    return True, None  # 默认通过


def check_product_against_pc_list(product, pc_list):
    """
    product 和整个 pc_list 的一对多整体检查，如总功耗、电源瓦数、内存插槽。
    """
    issues = []
    pc_products = Product.objects.filter(sku__in=pc_list)

    # === 1. 总功耗与电源瓦数 ===
    total_power = 0
    for p in pc_products:
        power_spec = ProductSpec.objects.filter(product=p, spec__spec='power').first()
        if power_spec:
            total_power += int(power_spec.value.value)

    # 加上当前新增产品的功耗
    product_power = ProductSpec.objects.filter(product=product, spec__spec='power').first()
    if product_power:
        total_power += int(product_power.value.value)

    # 查找电源
    psu_list = [p for p in pc_products if p.mainGroup.mainGroupName == 'Voedingen']
    if product.mainGroup.mainGroupName == 'Voedingen':
        psu_list.append(product)

    # 电源瓦数检查
    if psu_list:
        psu = psu_list[0]  # 默认取第一个 PSU
        psu_watt_spec = ProductSpec.objects.filter(product=psu, spec__spec='watt').first()
        if psu_watt_spec and int(psu_watt_spec.value.value) < total_power:
            issues.append(f"PSU wattage insufficient: {psu_watt_spec.value.value}W < total required {total_power}W")

    # === 2. 内存插槽检查 ===
    rams = [p for p in pc_products if p.mainGroup.mainGroupName == 'Geheugen']
    if product.mainGroup.mainGroupName == 'Geheugen':
        rams.append(product)

    mainboards = [p for p in pc_products if p.mainGroup.mainGroupName == 'Moederborden']
    if product.mainGroup.mainGroupName == 'Moederborden':
        mainboards.append(product)

    if mainboards:
        mainboard = mainboards[0]  # 默认取第一个主板
        ram_slots_spec = ProductSpec.objects.filter(product=mainboard, spec__spec='ram_slots').first()
        if ram_slots_spec and len(rams) > int(ram_slots_spec.value.value):
            issues.append(f"Too many RAM sticks: selected {len(rams)} sticks, but motherboard supports {ram_slots_spec.value.value} slots")

    # === TODO: 后续可扩展机箱空间等检查 ===

    return (False, issues) if issues else (True, None)


def product_is_compatible(product, pc_list):
    """
    综合函数，检查新加入的 product 是否和现有 pc_list 全部兼容。
    """

    # 一对一检查
    pc_products = Product.objects.filter(sku__in=pc_list)
    for p in pc_products:
        valid, message = check_pair_compatibility(product, p)
        if not valid:
            return False, [message]  # 返回不兼容原因

    # 一对多整体检查
    valid, issues = check_product_against_pc_list(product, pc_list)
    if not valid:
        return False, issues  # 返回所有发现的问题

    return True, []  # 全部通过
