import logging

import django_filters
import graphene
from graphene import relay
from graphene.types import ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from company.models import Company as CompanyModel


# Annex F - Company Data Service
# GraphQL data model
class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(required=True, lookup_expr='icontains')

    class Meta:
        model = CompanyModel
        fields = ['name', ]


class Company(DjangoObjectType):
    company_id = graphene.UUID(description='The UUID of the company', )
    name = graphene.String(description='The name of the company', )
    industry = graphene.String(description='The industry in which the company operates', )
    description = graphene.String(description='A description of the company', )
    exchange = graphene.String(description='The stock exchange in which the company is listed', )

    # TODO figure out the proper type for country
    # country = graphene.Enum(description='The country in which the company operates',)

    class Meta:
        model = CompanyModel
        description = 'General information about a company'


class CompanyNode(Company):
    id = relay.GlobalID(description='A global ID for reactive paging purposes', )

    class Meta:
        model = CompanyModel
        interfaces = (relay.Node,)
        description = 'A node that encapsulates the company to support data-driven React applications'


class CompanyQuery(ObjectType):
    company = graphene.Field(
        type=Company,
        description='Retrieve general information about a company using a UUID',
        company_id=graphene.UUID(required=True, description='The UUID of a company', ),
    )
    companies = DjangoFilterConnectionField(
        type=CompanyNode,
        description='Search for companies that contains the given name',
        filterset_class=CompanyFilter,
    )

    def resolve_company(self, info: ResolveInfo, company_id: graphene.UUID, **kwargs, ) -> Company:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        return CompanyModel.objects.get(company_id=company_id, )
