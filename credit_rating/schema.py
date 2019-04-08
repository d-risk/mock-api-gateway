import logging
from typing import List

import graphene
import graphene_django
import graphql
from graphene import relay

from credit_rating.models import CreditRating as CreditRatingEnum
from credit_rating.models import CreditRatingModel


class CreditRating(graphene_django.DjangoObjectType):
    class Meta:
        model = CreditRatingModel
        interfaces = (relay.Node,)
        description = 'A credit rating'


class CreditRatingQuery(graphene.ObjectType):
    ratings = graphene.List(
        of_type=graphene.NonNull(CreditRating),
        description='A list of credit ratings',
        required=True,
    )

    def resolve_ratings(self, info: graphql.ResolveInfo, **kwargs) -> List[CreditRatingModel]:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        result: List[CreditRatingModel] = []
        for rating in CreditRatingEnum:
            result.append(CreditRatingModel(order=rating.value, name=rating.readable_name))
        return result
