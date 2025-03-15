from django.db import models

# Brand model has no foreign key, it is a standalone model
class Brand(models.Model):
    brandId = models.IntegerField(primary_key=True)
    brandName = models.CharField(max_length=100)

    def __str__(self):
        return self.brandName

# MainGroup model has no foreign key, it is a standalone model
class MainGroup(models.Model):
    mainGroup = models.IntegerField(primary_key=True)
    mainGroupName = models.CharField(max_length=100)

    def __str__(self):
        return self.mainGroupName

# SubGroup model has a foreign key to MainGroup
class SubGroup(models.Model):
    subGroup = models.IntegerField(primary_key=True)
    subGroupName = models.CharField(max_length=100)
    mainGroup = models.ForeignKey(MainGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.subGroupName


# Product model has foreign keys to Brand, MainGroup, SubGroup and ComponentType
class Product(models.Model):
    sku = models.BigIntegerField(primary_key=True)
    productName = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    mainGroup = models.ForeignKey(MainGroup, on_delete=models.CASCADE)
    subGroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.productName

# Spec model has no foreign key, it is a standalone model
class Spec(models.Model):
    specId = models.IntegerField(primary_key=True)
    spec = models.CharField(max_length=100)
    mainSpec = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.spec

# SpecValue model has a foreign key to Spec
class SpecValue(models.Model):
    valueId = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100)
    trailer = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.value

# ProductSpec model has foreign keys to Product, Spec and SpecValue
class ProductSpec(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    spec = models.ForeignKey(Spec, on_delete=models.CASCADE)
    value = models.ForeignKey(SpecValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} - {self.spec}: {self.value}"


# CompatibilityRule model has foreign keys to ComponentType
class CompatibilityRule(models.Model):
    componentType1 = models.ForeignKey(MainGroup, related_name='source_rules', on_delete=models.CASCADE)
    componentType2 = models.ForeignKey(MainGroup, related_name='target_rules', on_delete=models.CASCADE)
    relationType = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.componentType1} -> {self.componentType2}: {self.relationType}={self.value}"

