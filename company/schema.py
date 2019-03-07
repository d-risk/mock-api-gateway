import logging

import django_filters
import graphene
import graphene_django
import graphql
from graphene import relay
from graphene_django import filter

from company.models import Company as CompanyModel


# Annex F - Company Data Service
# GraphQL data model
class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(required=True, lookup_expr='icontains')

    class Meta:
        model = CompanyModel
        fields = ['name', ]


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
        filterset_class=CompanyFilter,
    )

    def resolve_company(
            self,
            info: graphql.ResolveInfo,
            company_id: graphene.UUID,
            **kwargs,
    ) -> Company:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        return CompanyModel.objects.get(company_id=company_id, )
