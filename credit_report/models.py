from django.db import models
from django.utils.timezone import now

from financial_report.models import FinancialReport


# Create your models here.
# Annex G - Credit Report Service
# SQL data model
class CreditReport(models.Model):
    report_id = models.AutoField(primary_key=True, )
    company_id = models.UUIDField(db_index=True, editable=False, )
    probability_of_default = models.DecimalField(decimal_places=2, max_digits=9, editable=False, )
    credit_rating = models.CharField(max_length=5, editable=False, )
    date_time = models.DateTimeField(default=now, editable=False, )

    class Meta:
        db_table = 'app_credit_reports'
        ordering = ['-date_time', ]
