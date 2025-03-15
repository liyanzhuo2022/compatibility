from django.contrib import admin
from .models import Brand, MainGroup, SubGroup, ComponentType, Product, Spec, SpecValue, ProductSpec, CompatibilityRule

admin.site.register(Brand)
admin.site.register(MainGroup)
admin.site.register(SubGroup)
admin.site.register(ComponentType)
admin.site.register(Product)
admin.site.register(Spec)
admin.site.register(SpecValue)
admin.site.register(ProductSpec)
admin.site.register(CompatibilityRule)

