import uuid

from django.db import models
from django_countries import fields


# Annex F - Company Data Service
# SQL data model
class Company(models.Model):
    company_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, )
    name = models.TextField(db_index=True, default=None, unique=True, editable=False, )
    industry = models.TextField(db_index=True, default=None, editable=False, )
    description = models.TextField(default=None, editable=False, )
    exchange = models.TextField(db_index=True, default=None, editable=False, )
    country = fields.CountryField(db_index=True, default=None, editable=False, )

    class Meta:
        db_table = 'app_companies'
