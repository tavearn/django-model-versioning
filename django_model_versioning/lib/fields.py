from django.db.models.fields import UUIDField, BigIntegerField, IntegerField, CharField, BigAutoField

from lib.versioning_field import VersioningField


class VersionedBigIntegerField(VersioningField, BigIntegerField):
    replace_fields = [BigIntegerField, BigAutoField]
    pass


class VersionedIntegerField(VersioningField, IntegerField):
    replace_fields = [IntegerField]


class VersionedCharField(VersioningField, CharField):
    replace_fields = [CharField]


class VersionedUUIDField(VersioningField, UUIDField):
    replace_fields = [UUIDField]
