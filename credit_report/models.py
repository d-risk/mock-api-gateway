from django.db.models import Model, UUIDField, CharField, DateTimeField, DecimalField, ManyToManyField, \
    ForeignKey, PROTECT
from django.utils.timezone import now

from news.models import News


# Create your models here.
# Annex G - Credit Report Service
# SQL data model
class FinancialReport(Model):
    company_id = UUIDField(db_index=True)
    report_date = DateTimeField(default=now, )
    currency = CharField(max_length=5, )

    class Meta:
        db_table = 'app_financial_reports'


class CreditReport(Model):
    company_id = UUIDField(db_index=True, )
    credit_score = DecimalField(decimal_places=2, max_digits=9, )
    credit_rating = CharField(max_length=5, )
    report_date = DateTimeField(default=now, )
    financial_reports = ManyToManyField(FinancialReport, related_name='credit_reports', )
    news = ManyToManyField(News, related_name='credit_reports', )

    class Meta:
        db_table = 'app_credit_reports'


class FinancialData(Model):
    financial_report = ForeignKey(FinancialReport, on_delete=PROTECT, related_name='financial_data', )
    name = CharField(max_length=50, )
    value = DecimalField(decimal_places=9, max_digits=99, )

    class Meta:
        db_table = 'app_financial_data'
