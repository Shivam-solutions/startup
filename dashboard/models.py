from django.db import models

    # your existing fields...

# Starter models (extend as needed)
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
   
    # Sales Scheme
    sales_deal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sales_free = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Purchase Scheme
    purc_deal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purc_free = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    mrp = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sales_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    company = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    rec_date = models.DateField(null=True, blank=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    exp = models.DateField(null=True, blank=True)

    supplier = models.CharField(max_length=255, blank=True, null=True)
    inv_no = models.CharField(max_length=100, blank=True, null=True)
    inv_date = models.DateField(null=True, blank=True)
    rack_no = models.CharField(max_length=100, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name or self.code or "Stock #{}".format(self.pk)
