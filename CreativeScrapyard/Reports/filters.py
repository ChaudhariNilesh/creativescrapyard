import django_filters 

from Items.models import *


class ProductFilter(django_filters.FilterSet):
    crt_item_id = django_filters.NumberFilter(field_name='crt_item_id',lookup_expr='icontains')
    crt_item_name = django_filters.CharFilter(field_name='crt_item_name',lookup_expr='icontains')
    # crt_created_on = django_filters.NumberFilter(field_name='crt_created_on',lookup_expr='year')
    # crt_created_on__gt = django_filters.NumberFilter(field_name='crt_created_on',lookup_expr='year__gt')
    # crt_created_on__lt = django_filters.NumberFilter(field_name='crt_created_on',lookup_expr='year__lt')
    crt_created_on = django_filters.DateFromToRangeFilter(field_name='crt_created_on')
    crt_item_price = django_filters.RangeFilter(field_name='crt_item_price')
    crt_item_qty = django_filters.RangeFilter(field_name='crt_item_qty')

    class Meta:
        model = tbl_creativeitems_mst
        fields = ['crt_item_id','crt_item_name','crt_created_on','crt_sub_category','crt_item_status','crt_item_price','crt_item_qty']
