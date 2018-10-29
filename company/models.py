import uuid

from django.db.models import Model, UUIDField, TextField
from django_countries.fields import CountryField


# Annex F - Company Data Service
# SQL data model
class Company(Model):
    id = UUIDField(default=uuid.uuid4, editable=False, primary_key=True, )
    name = TextField(db_index=True, default=None, unique=True, )
    industry = TextField(db_index=True, default=None, )
    description = TextField(default=None, )
    exchange = TextField(db_index=True, default=None, )
    country = CountryField(db_index=True, default=None, )

    class Meta:
        db_table = 'app_companies'
