from django.contrib import admin

from fund.models import Fund


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'net_asset', 'cancel_nav', 'annual_efficiency')
    readonly_fields = ('name', 'reg_no', 'net_asset', 'cancel_nav', 'annual_efficiency', 'investment_manager',
                       'ins_inv_no', 'ret_inv_no')
    search_fields = ('name', 'investment_manager')
