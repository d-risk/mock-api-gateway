from django_filters import FilterSet, NumberFilter
from graphene import Node, ObjectType
from graphene_django import DjangoObjectType

from news.models import News


class NewsFilter(FilterSet):
    class Meta:
        model = News
        fields = ['date', ]

    year = NumberFilter(field_name='date', lookup_expr='year')
    from_year = NumberFilter(field_name='date', lookup_expr='year__gte')
    to_year = NumberFilter(field_name='date', lookup_expr='year__lte')


class NewsNode(DjangoObjectType):
    class Meta:
        model = News
        interfaces = [Node, ]


class NewsQuery(ObjectType):
    news = Node.Field(NewsNode, )
