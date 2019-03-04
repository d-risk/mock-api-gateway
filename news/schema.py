import logging

import graphene
from django_filters import FilterSet, NumberFilter
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from news.models import News as NewsModel


class NewsFilter(FilterSet):
    class Meta:
        model = NewsModel
        fields = ['date_time', ]

    year = NumberFilter(field_name='date_time', lookup_expr='year',
                        description='Filter out news snippets that does not match the year')
    from_year = NumberFilter(field_name='date_time', lookup_expr='year__gte',
                             description='Filter out news snippets that are older than the year')
    to_year = NumberFilter(field_name='date_time', lookup_expr='year__lte',
                           description='Filter out news snippets that newer than the year')


class News(DjangoObjectType):
    news_id = graphene.ID(description='The ID of the news snippet')
    company_id = graphene.UUID(description='The company, as identified by the UUID, of the news snippet')
    title = graphene.String(description='The title of the news snippet')
    date_time = graphene.DateTime(description='The date and time of the news snippet')
    snippet = graphene.String(description='A snippet of the news')
    url = graphene.String(description='The URL where the news originated')

    class Meta:
        model = NewsModel
        description = 'A news snippet'


class NewsNode(News):
    id = relay.GlobalID(description='A global ID for reactive paging purposes')

    class Meta:
        model = NewsModel
        interfaces = [graphene.Node, ]
        description = 'A node that encapsulates the news snippet to support data-driven React applications'


class NewsQuery(graphene.ObjectType):
    news = graphene.Field(
        type=News,
        description='Find a news snippet using an ID',
        news_id=graphene.ID(description='The ID of a news snippet'),
    )
    news_by_company = DjangoFilterConnectionField(
        type=NewsNode,
        order_by='-date_time',
        filterset_class=NewsFilter,
        description='Search for news snippets of a company (by the given UUID) that is sorted by date and time',
        company_id=graphene.UUID(description='The UUID of the company'),
    )

    def resolve_news(self, info: ResolveInfo, news_id=graphene.ID(description='description'), **kwargs):
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        NewsModel.objects.get(news_id=news_id)
