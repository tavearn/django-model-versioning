from typing import Optional, TYPE_CHECKING

from lib.versioning_options import VersioningOptions

if TYPE_CHECKING:
    from lib.types import VersionedModelInstance, PersistentFieldInstance


class VersionedModel:
    _versioning_options = None  # type: Optional[VersioningOptions]

    def __init__(self, *args, **kwargs):
        super(VersionedModel, self).__init__(*args, **kwargs)
        self._django_model_versioning_original_state = {}
        self.store_original_state()
        self._django_model_versioning_avoid_signal = False

    def save(self: 'VersionedModelInstance', *args, **kwargs):
        self._django_model_versioning_avoid_signal = kwargs.pop('django_model_versioning_avoid_signal', False)
        if self.versioned_fields_changed():
            # Set the primary key to None to generate a new model
            if self._meta.pk.attname != self._versioning_options.persistence_key:
                self.regenerate_persinstance_key()
            setattr(self, self._meta.pk.attname, None)
        super(VersionedModel, self).save(*args, **kwargs)

    def regenerate_persinstance_key(self: 'VersionedModelInstance') -> None:
        current_value = getattr(self, self._versioning_options.persistence_key)
        setattr(self, self._versioning_options.persistence_key,
                self.versioned_field.generate_new_version(current_value))

    def store_original_state(self) -> None:
        if self._versioning_options is None:
            return

        for versioned_field in self._versioning_options.versioned_fields:
            self._django_model_versioning_original_state[versioned_field] = getattr(self, versioned_field, None)

    def versioned_fields_changed(self) -> bool:
        return any(getattr(self, versioned_field) != self._django_model_versioning_original_state.get(versioned_field)
                   for versioned_field in self._versioning_options.versioned_fields)

    @property
    def versioned_field(self: 'VersionedModelInstance') -> 'PersistentFieldInstance':
        return self._meta.get_field(self._versioning_options.persistence_key)

    @classmethod
    def get_versioning_options(cls) -> VersioningOptions:
        if cls._versioning_options is None:
            raise Exception("_versioning_options needs to be defined. "
                            "Did you initialize your model using @register methoid?")
        return cls._versioning_options
