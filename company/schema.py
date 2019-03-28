import logging
from typing import List

import django_filters
import graphene
import graphene_django
import graphql
from django.db.models import QuerySet, functions
from graphene import relay
from graphene_django import filter

from company.models import Company as CompanyModel
from credit_report.models import CreditReport as CreditReportModel


# Annex F - Company Data Service
# GraphQL data model
class CompanyFilterByName(django_filters.FilterSet):
    name = django_filters.CharFilter(required=True, lookup_expr='istartswith')

    class Meta:
        model = CompanyModel
        fields = ['name', ]

    @property
    def qs(self):
        return super(CompanyFilterByName, self).qs.order_by(functions.Upper('name'))


class Company(graphene_django.DjangoObjectType):
    id = relay.GlobalID(description='A global ID for reactive paging purposes', )
    company_id = graphene.UUID(description='The UUID of the company', )
    name = graphene.String(description='The name of the company', )
    industry = graphene.String(description='The industry in which the company operates', )
    description = graphene.String(description='A description of the company', )
    exchange = graphene.String(description='The stock exchange in which the company is listed', )

    # TODO figure out the proper type for country
    # country = graphene.Enum(description='The country in which the company operates',)

    class Meta:
        model = CompanyModel
        interfaces = (relay.Node,)
        description = 'General information about a company'


class CompanyQuery(graphene.ObjectType):
    company = graphene.Field(
        type=Company,
        description='Retrieve general information about a company using a UUID',
        company_id=graphene.UUID(required=True, description='The UUID of a company', ),
    )
    companies_by_name = filter.DjangoFilterConnectionField(
        type=Company,
        description='Search for companies that contains the given name',
        filterset_class=CompanyFilterByName,
    )
    companies_by_ratings = graphene_django.DjangoConnectionField(
        type=Company,
        description='Search for companies that matches the given ratings',
        ratings=graphene.List(of_type=graphene.String, required=True, ),
    )

    def resolve_company(
            self,
            info: graphql.ResolveInfo,
            company_id: graphene.UUID,
            **kwargs,
    ) -> Company:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        return CompanyModel.objects.get(company_id=company_id, )

    def resolve_companies_by_ratings(
            self,
            info: graphql.ResolveInfo,
            ratings: graphene.List,
            **kwargs,
    ) -> List[Company]:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        companies: QuerySet = CompanyModel.objects.all()
        results: List[Company] = []
        for company in companies:
            credit_reports: QuerySet = CreditReportModel.objects.filter(company_id=company.company_id)
            credit_report: CreditReportModel = credit_reports.latest(field_name='date_time')
            if credit_report.credit_rating in ratings:
                results.append(company)
        return results
