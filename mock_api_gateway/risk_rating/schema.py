import logging
from typing import List

import graphene
import graphene_django
import graphql
from graphene import relay

from mock_api_gateway.risk_rating.models import RiskRating as RiskRatingEnum
from mock_api_gateway.risk_rating.models import RiskRatingModel


class RiskRating(graphene_django.DjangoObjectType):
    class Meta:
        model = RiskRatingModel
        interfaces = (relay.Node,)
        description = 'A risk rating'


class RiskRatingQuery(graphene.ObjectType):
    ratings = graphene.List(
        of_type=graphene.NonNull(RiskRating),
        description='A list of risk ratings',
        required=True,
    )

    def resolve_ratings(self, info: graphql.ResolveInfo, **kwargs) -> List[RiskRatingModel]:
        logging.debug(f'self={self}, info={info}, kwargs={kwargs}')
        result: List[RiskRatingModel] = []
        for rating in RiskRatingEnum:
            result.append(RiskRatingModel(order=rating.value, name=rating.readable_name))
        return result
