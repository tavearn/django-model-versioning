from django.db.models import Model, CharField, DateTimeField, DecimalField


class Tax(Model):
    name = CharField(max_length=255, blank=False, null=False)
    percentage_value = DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
