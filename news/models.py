from django.db.models import Model, TextField, URLField, DateTimeField, UUIDField
from django.utils.timezone import now


# Create your models here.
class News(Model):
    company_id = UUIDField(db_index=True, )
    title = TextField(db_index=True, )
    date_time = DateTimeField(default=now, )
    snippet = TextField()
    url = URLField()

    class Meta:
        db_table = 'app_news'
