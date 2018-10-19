from django.db.models import Model, UUIDField, CharField, DateTimeField, DecimalField, ManyToManyField
from django.utils.timezone import now

from financial_report.models import FinancialReport
from news.models import News


# Create your models here.
# Annex G - Credit Report Service
# SQL data model
class CreditReport(Model):
    company_id = UUIDField(db_index=True, )
    probability_of_default = DecimalField(decimal_places=2, max_digits=9, )
    credit_rating = CharField(max_length=5, )
    date_time = DateTimeField(default=now, )
    financial_reports = ManyToManyField(FinancialReport, related_name='credit_reports', )
    news = ManyToManyField(News, related_name='credit_reports', )

    class Meta:
        db_table = 'app_credit_reports'
