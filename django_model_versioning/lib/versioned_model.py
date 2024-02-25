from typing import Optional, TYPE_CHECKING

from lib.versioning_options import VersioningOptions

if TYPE_CHECKING:
    from lib.types import VersionedModelInstance


class VersionedModel:
    _versioning_options = None  # type: Optional[VersioningOptions]

    def __init__(self, *args, **kwargs):
        super(VersionedModel, self).__init__(*args, **kwargs)
        self._django_model_versioning_avoid_signal = False

    def save(self: 'VersionedModelInstance', *args, **kwargs):
        self._django_model_versioning_avoid_signal = kwargs.pop('django_model_versioning_avoid_signal', False)
        super(VersionedModel, self).save(*args, **kwargs)

    @classmethod
    def get_versioning_options(cls) -> VersioningOptions:
        if cls._versioning_options is None:
            raise Exception("_versioning_options needs to be defined. "
                            "Did you initialize your model using @register methoid?")
        return cls._versioning_options
