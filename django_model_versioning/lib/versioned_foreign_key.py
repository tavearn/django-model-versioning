from typing import TYPE_CHECKING

from django.db.models import ForeignKey, Q

from lib.config import Config

if TYPE_CHECKING:
    from lib.types import VersionedModelType


class VersionedForeignKey(ForeignKey):
    # SuperClass is called within a child function
    # noinspection PyMissingConstructor
    def __init__(
            self,
            to: 'VersionedModelType',
            *args,
            **kwargs,
    ):
        self._reference_model = to
        super(VersionedForeignKey, self).__init__(
            to,
            *args,
            **kwargs,
        )

    def _check_unique_target(self):
        return []

    def get_forward_related_filter(self, obj):
        """
        Return the keyword arguments that when supplied to
        self.model.object.filter(), would select all instances related through
        this field to the remote obj. This is used to build the querysets
        returned by related descriptors. obj is an instance of
        self.related_field.model.
        """
        return {
            "%s__%s" % (self.name, rh_field.name): getattr(obj, rh_field.attname)
            for _, rh_field in self.related_fields
        }

    def get_reverse_related_filter(self, obj):
        """
        Complement to get_forward_related_filter(). Return the keyword
        arguments that when passed to self.related_field.model.object.filter()
        select all instances of self.related_field.model related through
        this field to obj. obj is an instance of self.model.
        """
        foreign_key_value = getattr(obj, self.attname)
        return Q(**{
            Config.persisted_field_name: foreign_key_value
        }) & Q(**{
            Config.version_field_name: None
        })
