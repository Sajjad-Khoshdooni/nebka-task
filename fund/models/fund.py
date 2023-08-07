from django.db import models


class Fund(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=256, db_index=True)
    reg_no = models.PositiveIntegerField(unique=True)
    net_asset = models.BigIntegerField(null=True)
    cancel_nav = models.IntegerField(null=True)
    annual_efficiency = models.DecimalField(max_digits=10, decimal_places=4, null=True)

    investment_manager = models.CharField(max_length=256, null=True)
    ins_inv_no = models.IntegerField(null=True)
    ret_inv_no = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    