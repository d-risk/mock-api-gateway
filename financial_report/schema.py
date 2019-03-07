import logging
from typing import List

import django_filters
import graphene
import graphene_django
import graphql
from graphene import relay
from graphene_django import filter

from financial_report.models import FinancialData as FinancialDataModel
from financial_report.models import FinancialRatio as FinancialRatioModel
from financial_report.models import FinancialReport as FinancialReportModel


class FinancialReportFilter(django_filters.FilterSet):
    company_id = django_filters.UUIDFilter(required=True, label='The UUID of the company', )
    year = django_filters.NumberFilter(
        field_name='date_time',
        lookup_expr='year',
        label='Filter out financial reports that does not match the year',
    )
    from_year = django_filters.NumberFilter(
        field_name='date_time',
        lookup_expr='year__gte',
        label='Filter out financial reports that are older than the year',
    )
    to_year = django_filters.NumberFilter(
        field_name='date_time',
        lookup_expr='year__lte',
        label='Filter out financial reports that newer than the year',
    )

    class Meta:
        model = FinancialReportModel
        fields = ['company_id', ]

    @property
    def qs(self):
        return super(FinancialReportFilter, self).qs.order_by('-date_time', )


class FinancialData(graphene_django.DjangoObjectType):
    id = graphene.ID(description='The ID of the financial data', required=True, )
    name = graphene.String(description='The name of the financial data', required=True, )
    value = graphene.Float(description='The value of the financial data', required=True, )

    class Meta:
        model = FinancialDataModel
        exclude_fields = ('financial_report',)
        description = 'A financial data'


class FinancialRatio(graphene_django.DjangoObjectType):
    id = graphene.ID(description='The ID of the financial ratio', required=True, )
    name = graphene.String(description='The name of the financial ratio', required=True, )
    value = graphene.Float(description='The value of the financial ratio', required=True, )
    formula = graphene.String(description='The formula to calculate the value', required=True, )

    class Meta:
        model = FinancialRatioModel
        exclude_fields = ('financial_report',)
        description = 'A financial ratio'


class FinancialReport(graphene_django.DjangoObjectType):
    report_id = graphene.ID(description='The ID of the financial report', required=True, )
    company_id = graphene.UUID(
        description='The company, as identified by the UUID, of the financial report',
        required=True,
    )
    date_time = graphene.DateTime(description='The date and time of the report', required=True, )
    currency = graphene.String(description='The currency that the report uses', required=True, )
    financial_data = graphene.List(
        of_type=graphene.NonNull(of_type=FinancialData),
        description='A list of financial data',
        required=True,
    )
    financial_ratios = graphene.List(
        of_type=graphene.NonNull(of_type=FinancialRatio),
        description='A list of financial ratios',
        required=True,
    )

    class Meta:
        model = FinancialReportModel
        description = 'A financial report'

    def resolve_financial_data(
            self: FinancialReportModel,
            info: graphql.ResolveInfo,
            **kwargs,
    ) -> List[FinancialDataModel]:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        return self.financial_data.all()

    def resolve_financial_ratios(
            self: FinancialReportModel,
            info: graphql.ResolveInfo,
            **kwargs,
    ) -> List[FinancialRatioModel]:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        return self.financial_ratios.all()


class FinancialReportNode(FinancialReport):
    id = relay.GlobalID(description='A global ID that relay uses for reactive paging purposes', )

    class Meta:
        model = FinancialReportModel
        interfaces = (relay.Node,)
        description = 'A node that encapsulates the financial report to support data-driven React applications'


class FinancialReportQuery(graphene.ObjectType):
    financial_report = graphene.Field(
        type=FinancialReport,
        description='Find a financial report using an ID',
        report_id=graphene.ID(required=True, description='The ID of a financial report', ),
    )
    financial_reports_by_company = filter.DjangoFilterConnectionField(
        type=FinancialReportNode,
        description='Search for a list of financial report of a company (by the given UUID) that is ordered by date '
                    'and time',
        filterset_class=FinancialReportFilter,
    )

    def resolve_financial_report(
            self,
            info: graphql.ResolveInfo,
            report_id: graphene.ID,
            **kwargs,
    ) -> FinancialReport:
        logging.debug(f'self={self}, info={info}, news_id={report_id} kwargs={kwargs}')
        return FinancialReportModel.objects.get(report_id=report_id, )
