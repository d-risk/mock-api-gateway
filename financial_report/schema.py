from django_filters import FilterSet, NumberFilter
from graphene import Node, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

import financial_report.models
from financial_report.models import FinancialReport


class FinancialReportFilter(FilterSet):
    class Meta:
        model = FinancialReport
        fields = ['date_time', ]

    year = NumberFilter(field_name='date_time', lookup_expr='year')
    from_year = NumberFilter(field_name='date_time', lookup_expr='year__gte')
    to_year = NumberFilter(field_name='date_time', lookup_expr='year__lte')

    @property
    def qs(self: FilterSet):
        if not hasattr(self, '_qs'):
            qs = self.queryset.all().order_by('-date_time')
            if self.is_bound:
                # ensure form validation before filtering
                self.errors
                qs = self.filter_queryset(qs)
            self._qs = qs
        return self._qs


class FinancialReportNode(DjangoObjectType):
    class Meta:
        model = FinancialReport
        interfaces = [Node, ]


class FinancialData(DjangoObjectType):
    class Meta:
        model = financial_report.models.FinancialData


class FinancialRatio(DjangoObjectType):
    class Meta:
        model = financial_report.models.FinancialRatio


class FinancialReportQuery(ObjectType):
    financial_report = Node.Field(FinancialReportNode, )
    financial_reports = DjangoFilterConnectionField(
        FinancialReportNode,
        order_by='-date_time',
        filterset_class=FinancialReportFilter,
    )
