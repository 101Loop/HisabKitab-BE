from .models import TransactionDetails
from django_filters import FilterSet


class RangeFiltering(FilterSet):

    from django_filters.rest_framework import NumberFilter, DateFilter

    start_date = DateFilter(name='transaction_date', lookup_expr='gte')
    end_date = DateFilter(name='transaction_date', lookup_expr='lte')
    start_amount = NumberFilter(name='amount', lookup_expr='gte')
    end_amount = NumberFilter(name='amount', lookup_expr='lte')

    class Meta:
        model = TransactionDetails
        fields = ('start_date', 'end_date', 'start_amount', 'end_amount')
