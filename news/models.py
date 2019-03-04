from django.db import models
from django.utils.timezone import now


# Create your models here.
class News(models.Model):
    company_id = models.UUIDField(db_index=True, editable=False, )
    title = models.TextField(db_index=True, editable=False, )
    date_time = models.DateTimeField(db_index=True, default=now, editable=False, )
    snippet = models.TextField(editable=False, )
    url = models.URLField(editable=False, )

    class Meta:
        db_table = 'app_news'
