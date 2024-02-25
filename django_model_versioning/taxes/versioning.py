from lib.register import register
from lib.versioning_options import VersioningOptions
from taxes.models import Tax


@register(Tax)
class TaxVersioningOptions(VersioningOptions):
    versioned_fields = ('percentage_value',)
