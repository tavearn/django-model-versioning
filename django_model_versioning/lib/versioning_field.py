from typing import Type, TYPE_CHECKING

from django.db.models import Field

# If this import doesn't happen within TYPE_CHECKING, for some reasons, Django doesn't dectect the
# new field when generating migrations
if TYPE_CHECKING:
    from lib.types import PersistentFieldInstance, VersionedModelInstance


class VersioningField:
    replace_fields = []

    @classmethod
    def of(cls, original_field: Type[Field]):
        # We need to import fields to make them discoverable
        # noinspection PyUnresolvedReferences
        import lib.fields
        replace_array = cls.__subclasses__()
        for field in replace_array:
            if original_field in field.replace_fields:
                return field
        raise Exception(f"Persistent field not supported for {original_field}")


    # TODO: probably requires a post_save signal instead
    def pre_save(self: 'PersistentFieldInstance', model_instance: 'VersionedModelInstance', add):
        super(VersioningField, self).pre_save(model_instance, add)
        current_value = getattr(model_instance, self.attname)

        if current_value is not None:
            return

        persistent_key = model_instance.get_versioning_options().persistence_key
        persistent_field = model_instance._meta.get_field(persistent_key)

        # Ensure any `pre_save` code has been executed on the original field
        persistent_field.pre_save(model_instance, add)

        id_value = getattr(model_instance, persistent_key)

        setattr(model_instance, self.attname, id_value)
