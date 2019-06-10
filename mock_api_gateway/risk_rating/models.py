import enum
from typing import List

from django.db import models


# Create your models here.
@enum.unique
class RiskRating(enum.IntEnum):
    AAA = 1,
    AA_PLUS = 2,
    AA = 3,
    AA_MINUS = 4,
    A_PLUS = 5,
    A = 6,
    A_MINUS = 7,
    BBB_PLUS = 8,
    BBB = 9,
    BBB_MINUS = 10,
    BB_PLUS = 11,
    BB = 12,
    BB_MINUS = 13,
    B_PLUS = 14,
    B = 15,
    B_MINUS = 16,
    CCC_PLUS = 17,
    CCC = 18,
    CCC_MINUS = 19,
    CC = 20,
    C = 21,
    D = 22,

    @property
    def readable_name(self: 'RiskRating') -> str:
        return super(RiskRating, self).name.replace('_PLUS', '+').replace('_MINUS', '-')

    @classmethod
    def as_list(cls: 'RiskRating') -> List['RiskRating']:
        return [x for x in RiskRating]


class RiskRatingModel(models.Model):
    order = models.IntegerField(primary_key=True, editable=False, )
    name = models.CharField(db_index=True, max_length=5, default=None, editable=False, )

    class Meta:
        db_table = 'app_risk_ratings'
