import datetime
import logging
from datetime import timezone
from random import uniform, choice

import django_filters
import graphene
import graphene_django
import graphql
from graphene import relay
from graphene_django import filter

from mock_api_gateway.company.models import Company
from mock_api_gateway.risk_rating.models import RiskRating
from mock_api_gateway.risk_report.models import RiskReport as RiskReportModel


# GraphQL data model
class RiskReportFilter(django_filters.FilterSet):
    company_id = django_filters.UUIDFilter(required=True, label='The UUID of the company', )
    year = django_filters.NumberFilter(
        field_name='date_time',
        lookup_expr='year',
        label='Filter out news snippets that does not match the year',
    )

    class Meta:
        model = RiskReportModel
        fields = ['company_id', ]

    @property
    def qs(self):
        return super(RiskReportFilter, self).qs.order_by('-date_time', )


class RiskReport(graphene_django.DjangoObjectType):
    id = relay.GlobalID(description='A global ID that relay uses for reactive paging purposes', )
    report_id = graphene.ID(description='The ID of the risk report', required=True, )
    company_id = graphene.UUID(
        description='The company, as identified by the UUID, of the risk report',
        required=True,
    )
    probability_of_default = graphene.Float(description='The probability of default of the company', required=True, )
    risk_rating = graphene.String(description='The risk rating of the company', required=True, )
    date_time = graphene.DateTime(description='The date and time of the risk report', required=True, )

    class Meta:
        model = RiskReportModel
        interfaces = (relay.Node,)
        description = 'A risk report'


class RiskReportQuery(graphene.ObjectType):
    risk_report = graphene.Field(
        type=RiskReport,
        description='Find a risk report using an ID',
        report_id=graphene.ID(required=True, description='The ID of the risk report', )
    )
    risk_reports_by_company = filter.DjangoFilterConnectionField(
        type=RiskReport,
        description='Search for a list of risk report of a company (by the given UUID) that is ordered by date and '
                    'time',
        filterset_class=RiskReportFilter,
    )

    def resolve_risk_report(
            self,
            info: graphql.ResolveInfo,
            report_id: graphene.ID,
            **kwargs,
    ) -> RiskReport:
        logging.debug(f'self={self}, info={info}, report_id={report_id}, kwargs={kwargs}')
        return RiskReportModel.objects.get(report_id=report_id, )


class CustomRiskReport(graphene.Mutation):
    Output = RiskReport

    class Arguments:
        company_id = graphene.UUID(description='The UUID of a company', required=True, )
        years = graphene.Int(description='Use the average of the past number of years', required=True, )

    def mutate(
            self,
            info: graphql.ResolveInfo,
            company_id: graphene.UUID,
            years: graphene.Int,
            **kwargs,
    ) -> RiskReport:
        logging.debug(f"self={self}, info={info}, company_id={company_id}, years={years}, kwargs={kwargs}")
        company = Company.objects.get(company_id=company_id)
        date_time = datetime.datetime.now(tz=timezone.utc)
        risk_report = RiskReportModel(
            company_id=company.company_id,
            probability_of_default=uniform(0, 1),
            risk_rating=choice([rating for rating in RiskRating]).readable_name,
            date_time=date_time,
        )
        logging.debug(f"risk_report={risk_report}")
        return risk_report


class RiskReportMutation(graphene.ObjectType):
    custom_risk_report = CustomRiskReport.Field(
        description="Customize a risk report for a company using the average of the past number of years",
        required=True,
    )
