
    first_name = django_filters.CharFilter(field_name='first_name',lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name',lookup_expr='icontains')