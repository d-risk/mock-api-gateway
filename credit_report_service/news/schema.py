import logging

import django_filters
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import ResolveInfo

from credit_report_service.news.models import News as NewsModel


class NewsFilter(django_filters.FilterSet):
    company_id = django_filters.UUIDFilter(required=True, label='The UUID of the company', )
    year = django_filters.NumberFilter(
        field_name='date_time',
        lookup_expr='year',
        label='Filter out news snippets that does not match the year',
    )
    from_year = django_filters.NumberFilter(
        field_name='date_time',
        lookup_expr='year__gte',
        label='Filter out news snippets that are older than the year',
    )
    to_year = django_filters.NumberFilter(
        field_name='date_time',
        lookup_expr='year__lte',
        label='Filter out news snippets that newer than the year',
    )

    class Meta:
        model = NewsModel
        fields = ['company_id', ]

    @property
    def qs(self):
        return super(NewsFilter, self).qs.order_by('-date_time', )


class News(DjangoObjectType):
    id = relay.GlobalID(description='A global ID that relay uses for reactive paging purposes', )
    news_id = graphene.ID(description='The ID of the news snippet', required=True, )
    company_id = graphene.UUID(
        description='The company, as identified by the UUID, of the news snippet',
        required=True,
    )
    title = graphene.String(description='The title of the news snippet', required=True, )
    date_time = graphene.DateTime(description='The date and time of the news snippet', required=True, )
    snippet = graphene.String(description='A snippet of the news', required=True, )
    url = graphene.String(description='The URL where the news originated', required=True, )

    class Meta:
        model = NewsModel
        interfaces = (relay.Node,)
        description = 'A news snippet'


class NewsQuery(graphene.ObjectType):
    news = graphene.Field(
        type=News,
        description='Find a news snippet using an ID',
        news_id=graphene.ID(required=True, description='The ID of a news snippet', ),
    )
    news_by_company = DjangoFilterConnectionField(
        type=News,
        description='Search for news snippets of a company (by the given UUID) that is ordered by date and time',
        filterset_class=NewsFilter,
    )

    def resolve_news(
            self,
            info: ResolveInfo,
            news_id: graphene.ID,
            **kwargs,
    ) -> News:
        logging.debug(f'self={self}, info={info}, news_id={news_id} kwargs={kwargs}')
        return NewsModel.objects.get(news_id=news_id, )
