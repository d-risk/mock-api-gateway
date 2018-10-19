from django_filters import FilterSet, NumberFilter
from graphene import Node, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from news.models import News


class NewsFilter(FilterSet):
    class Meta:
        model = News
        fields = ['date_time', ]

    year = NumberFilter(field_name='date_time', lookup_expr='year')
    from_year = NumberFilter(field_name='date_time', lookup_expr='year__gte')
    to_year = NumberFilter(field_name='date_time', lookup_expr='year__lte')


class NewsNode(DjangoObjectType):
    class Meta:
        model = News
        interfaces = [Node, ]


class NewsQuery(ObjectType):
    news = Node.Field(NewsNode, )
    credit_reports = DjangoFilterConnectionField(
        NewsNode,
        order_by='-date_time',
        filterset_class=NewsFilter,
    )
