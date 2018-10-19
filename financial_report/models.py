from django.db.models import Model, UUIDField, DateTimeField, CharField, ForeignKey, PROTECT, DecimalField
from django.utils.timezone import now


# Create your models here.
class FinancialReport(Model):
    company_id = UUIDField(db_index=True)
    date_time = DateTimeField(default=now, )
    currency = CharField(max_length=5, )

    class Meta:
        db_table = 'app_financial_reports'


class FinancialData(Model):
    financial_report = ForeignKey(FinancialReport, on_delete=PROTECT, related_name='financial_data', )
    name = CharField(max_length=50, )
    value = DecimalField(decimal_places=9, max_digits=99, )

    class Meta:
        db_table = 'app_financial_data'


class FinancialRatio(Model):
    financial_report = ForeignKey(FinancialReport, on_delete=PROTECT, related_name='financial_ratios', )
    name = CharField(max_length=50, )
    value = DecimalField(decimal_places=9, max_digits=99, )

    class Meta:
        db_table = 'app_financial_ratios'
