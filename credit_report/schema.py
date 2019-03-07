import logging

import django_filters
import graphene
import graphene_django
import graphql
from graphene import relay
from graphene_django import filter

from credit_report.models import CreditReport as CreditReportModel


# Annex G - Credit Report Service
# GraphQL data model
class CreditReportFilter(django_filters.FilterSet):
    company_id = django_filters.UUIDFilter(required=True, label='The UUID of the company', )
    year = django_filters.NumberFilter(
        field_name='date_time',
        lookup_expr='year',
        label='Filter out news snippets that does not match the year',
    )

    class Meta:
        model = CreditReportModel
        fields = ['company_id', ]

    @property
    def qs(self):
        return super(CreditReportFilter, self).qs.order_by('-date_time', )


class CreditReport(graphene_django.DjangoObjectType):
    report_id = graphene.ID(description='The ID of the credit report', required=True, )
    company_id = graphene.UUID(
        description='The company, as identified by the UUID, of the credit report',
        required=True,
    )
    probability_of_default = graphene.Float(description='The probability of default of the company', required=True, )
    credit_rating = graphene.String(description='The credit rating of the company', required=True, )
    date_time = graphene.DateTime(description='The date and time of the credit report', required=True, )

    class Meta:
        model = CreditReportModel
        description = 'A credit report'


class CreditReportNode(CreditReport):
    id = relay.GlobalID(description='A global ID that relay uses for reactive paging purposes', )

    class Meta:
        model = CreditReportModel
        interfaces = (relay.Node,)
        description = 'A node that encapsulates the credit report to support data-driven React applications'


class CreditReportQuery(graphene.ObjectType):
    credit_report = graphene.Field(
        type=CreditReport,
        description='Find a credit report using an ID',
        report_id=graphene.ID(required=True, description='The ID of the credit report', )
    )
    credit_reports_by_company = filter.DjangoFilterConnectionField(
        type=CreditReportNode,
        description='Search for a list of credit report of a company (by the given UUID) that is ordered by date and '
                    'time',
        filterset_class=CreditReportFilter,
    )
    custom_credit_report = graphene.Field(
        type=CreditReport,
        description='Get a custom credit report for a company using the average of the past number of years',
        company_id=graphene.UUID(description='The UUID of the company', required=True, ),
        years=graphene.Int(description='Use the average of the past number of years', required=True, ),
    )

    def resolve_credit_report(
            self,
            info: graphql.ResolveInfo,
            report_id: graphene.ID,
            **kwargs,
    ) -> CreditReportModel:
        logging.debug(f'self={self}, info={info}, report_id={report_id} kwargs={kwargs}')
        return CreditReportModel.objects.get(report_id=report_id, )
