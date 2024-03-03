from django.db.models import Model, CharField, IntegerField, DateTimeField, DO_NOTHING

from lib.versioned_foreign_key import VersionedForeignKey
from taxes.models import Tax


class Product(Model):
    name = CharField(max_length=255, null=False, blank=False)
    price = IntegerField(null=False, default=0)

    tax = VersionedForeignKey(Tax, on_delete=DO_NOTHING)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
