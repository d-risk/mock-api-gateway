import uuid

from django.db.models import Model, UUIDField, TextField
from django_countries.fields import CountryField


# Annex F - Company Data Service
# SQL data model
class Company(Model):
    company_id = UUIDField(default=uuid.uuid4, editable=False, primary_key=True, )
    name = TextField(db_index=True, default=None, unique=True, editable=False, )
    industry = TextField(db_index=True, default=None, editable=False, )
    description = TextField(default=None, editable=False, )
    exchange = TextField(db_index=True, default=None, editable=False, )
    country = CountryField(db_index=True, default=None, editable=False, )

    class Meta:
        db_table = 'app_companies'
