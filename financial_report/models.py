from django.db import models
from django.db.models import Model, PROTECT
from django.utils.timezone import now


# Create your models here.
class FinancialReport(models.Model):
    report_id = models.AutoField(primary_key=True, )
    company_id = models.UUIDField(db_index=True, editable=False, )
    date_time = models.DateTimeField(db_index=True, default=now, editable=False, )
    currency = models.CharField(max_length=5, editable=False, )

    class Meta:
        db_table = 'app_financial_reports'
        ordering = ['-date_time', ]


class FinancialData(models.Model):
    financial_report = models.ForeignKey(
        FinancialReport,
        on_delete=PROTECT,
        related_name='financial_data',
        editable=False,
    )
    name = models.CharField(max_length=50, editable=False, )
    value = models.DecimalField(decimal_places=9, max_digits=99, editable=False, )

    class Meta:
        db_table = 'app_financial_data'


class FinancialRatio(models.Model):
    financial_report = models.ForeignKey(
        FinancialReport,
        on_delete=PROTECT,
        related_name='financial_ratios',
        editable=False,
    )
    name = models.CharField(max_length=50, editable=False, )
    value = models.DecimalField(decimal_places=9, max_digits=99, editable=False, )
    formula = models.TextField(editable=False, )

    class Meta:
        db_table = 'app_financial_ratios'
