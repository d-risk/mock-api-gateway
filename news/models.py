from django.db.models import Model, TextField, URLField, DateTimeField, UUIDField
from django.utils.timezone import now


# Create your models here.
class News(Model):
    company_id = UUIDField(db_index=True, editable=False, )
    title = TextField(db_index=True, editable=False, )
    date_time = DateTimeField(default=now, editable=False, )
    snippet = TextField(editable=False, )
    url = URLField(editable=False, )

    class Meta:
        db_table = 'app_news'
