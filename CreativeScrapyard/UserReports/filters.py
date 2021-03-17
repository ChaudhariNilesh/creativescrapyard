import django_filters 

from Items.models import *
from Authentication.models import User
from Order.models import *
from CustomAdmin.models import *

from django import forms
class ProductFilter(django_filters.FilterSet):
    crt_item_SKU = django_filters.CharFilter(field_name='crt_item_SKU',lookup_expr='icontains')
    crt_item_name = django_filters.CharFilter(field_name='crt_item_name',lookup_expr='icontains')
    # crt_created_on = django_filters.NumberFilter(field_name='crt_created_on',lookup_expr='year')
    # crt_created_on__gt = django_filters.NumberFilter(field_name='crt_created_on',lookup_expr='year__gt')
    # crt_created_on__lt = django_filters.NumberFilter(field_name='crt_created_on',lookup_expr='year__lt')
    crt_created_on = django_filters.DateFromToRangeFilter(field_name='crt_created_on')
    crt_item_price = django_filters.RangeFilter(field_name='crt_item_price')
    crt_item_qty = django_filters.RangeFilter(field_name='crt_item_qty')
    crt_sub_category  = django_filters.ModelMultipleChoiceFilter(queryset=tbl_crt_categories.objects.all(),field_name="crt_sub_category__crt_category__crt_category_name",widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = tbl_creativeitems_mst
        fields = ['crt_item_SKU','crt_item_name','crt_created_on','crt_sub_category','crt_item_status','crt_item_price','crt_item_qty']

class ScrapItemFilter(django_filters.FilterSet):
    scp_item_SKU = django_filters.CharFilter(field_name='scp_item_SKU',lookup_expr='icontains')
    scp_item_name = django_filters.CharFilter(field_name='scp_item_name',lookup_expr='icontains')
    # scp_created_on = django_filters.NumberFilter(field_name='scp_created_on',lookup_expr='year')
    # scp_created_on__gt = django_filters.NumberFilter(field_name='scp_created_on',lookup_expr='year__gt')
    # scp_created_on__lt = django_filters.NumberFilter(field_name='scp_created_on',lookup_expr='year__lt')
    scp_created_on = django_filters.DateFromToRangeFilter(field_name='scp_created_on')
    scp_item_price = django_filters.RangeFilter(field_name='scp_item_price')
    scp_item_qty = django_filters.RangeFilter(field_name='scp_item_qty')
    scp_sub_category  = django_filters.ModelMultipleChoiceFilter(queryset=MainScrapCategory.objects.all(),field_name="scp_sub_category__scp_category__scp_category_name",widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = tbl_scrapitems
        fields = ['scp_item_SKU','scp_item_name','scp_created_on','scp_sub_category','scp_item_status','scp_item_price','scp_item_qty']



STATUS_CHOICES = (
    (True, 'Active'),
    (False, 'Inactive'),
)

VERIFIED_CHOICES = (
    (True, 'Verified'),
    (False, 'Unverified'),
)

ITEM_STATUS = (
    (1, "Pending"),
    (2, "Completed"),
    (3, "Cancelled"),
    (4, "Failed"),
    (5, "Returned"),
)

PAYMENT_MODE = (
    ("PPI", "Paytm Wallet"),
    ("UPI", "UPI"),
    ("CC", "Credit Card"),
    ("DC", "Debit Card"),
    ("NB", "Net Banking"),
)
class OrderFilter(django_filters.FilterSet):

    seller_name = django_filters.CharFilter(field_name='crt_item_mst__user__username',lookup_expr='icontains')
    buyer_name = django_filters.CharFilter(field_name='order__person_name',lookup_expr='icontains')
    sub_cat  = django_filters.ModelMultipleChoiceFilter(queryset=tbl_crt_subcategories.objects.all(),to_field_name='crt_sub_category_name',field_name="crt_item_mst__crt_sub_category__crt_sub_category_name")
    item_name = django_filters.CharFilter(field_name='crt_item_mst__crt_item_name',lookup_expr='icontains')
    item_status = django_filters.ChoiceFilter(field_name='item_status',choices=ITEM_STATUS)
    unit_price = django_filters.RangeFilter(field_name='unit_price')
    crt_item_qty = django_filters.RangeFilter(field_name='crt_item_qty')
    order_date = django_filters.DateFromToRangeFilter(field_name='order__order_date')
    delivery_date = django_filters.DateFromToRangeFilter(field_name='order__delivery_date')
    # pay_mode = django_filters.ChoiceFilter(field_name='order__payment__payment_mode',choices=PAYMENT_MODE)
    sub_cat  = django_filters.ModelMultipleChoiceFilter(queryset=tbl_crt_categories.objects.all(),to_field_name='crt_category_name',field_name="crt_item_mst__crt_sub_category__crt_category__crt_category_name",widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = tbl_orders_details
        fields = ['seller_name','buyer_name','item_name','item_status','unit_price','crt_item_qty','order_date','delivery_date','sub_cat']