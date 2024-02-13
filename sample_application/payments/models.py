from django.db.models import Model, IntegerField, ForeignKey, DO_NOTHING, DateTimeField

from taxes.models import Tax


class Payment(Model):
    amount = IntegerField()

    tax = ForeignKey(Tax, on_delete=DO_NOTHING)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
