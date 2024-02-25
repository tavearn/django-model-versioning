from typing import Optional

from lib.versioning_options import VersioningOptions


class VersionedModel:
    _versioning_options = None  # type: Optional[VersioningOptions]

    @classmethod
    def get_versioning_options(cls) -> VersioningOptions:
        if cls._versioning_options is None:
            raise Exception("_versioning_options needs to be defined. "
                            "Did you initialize your model using @register methoid?")
        return cls._versioning_options
