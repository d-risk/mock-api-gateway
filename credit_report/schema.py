import graphene
from django_filters import FilterSet
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from credit_report.models import CreditReport
from financial_report.schema import FinancialReportFilter, FinancialReportNode
from news.schema import NewsNode, NewsFilter


# Annex G - Credit Report Service
# GraphQL data model
class CreditReportFilter(FilterSet):
    class Meta:
        model = CreditReport
        fields = ['company_id', ]

    @property
    def qs(self: FilterSet):
        if not hasattr(self, '_qs'):
            qs = self.queryset.all().order_by('-date_time')
            if self.is_bound:
                # ensure form validation before filtering
                self.errors()
                qs = self.filter_queryset(qs)
            self._qs = qs
        return self._qs


class CreditReportNode(DjangoObjectType):
    class Meta:
        model = CreditReport
        interfaces = [Node, ]

    financial_reports = DjangoFilterConnectionField(
        FinancialReportNode,
        order_by='-date_time',
        filterset_class=FinancialReportFilter,
    )
    news = DjangoFilterConnectionField(
        NewsNode,
        order_by='-date_time',
        filterset_class=NewsFilter,
    )


class CreditReportQuery(graphene.ObjectType):
    credit_reports = DjangoFilterConnectionField(
        CreditReportNode,
        order_by='-date_time',
        filterset_class=CreditReportFilter,
    )
