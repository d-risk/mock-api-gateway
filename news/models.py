from django.db.models import Model, TextField, URLField, DateTimeField
from django.utils.timezone import now


# Create your models here.
class News(Model):
    title = TextField(db_index=True, )
    date = DateTimeField(default=now, )
    snippet = TextField()
    url = URLField()

    class Meta:
        db_table = 'app_news'
