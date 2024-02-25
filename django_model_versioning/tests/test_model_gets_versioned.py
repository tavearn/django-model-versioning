from django.test import TestCase

from taxes.models import Tax


class TestModelGetsVersioned(TestCase):
    def __init__(self, *args, **kwargs):
        self.tax = None
        super(TestModelGetsVersioned, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.tax = Tax.objects.create(
            name='Food Tax',
            percentage_value=12.4
        )

    # noinspection PyMethodMayBeStatic
    def test_check_model_exists(self):
        assert Tax.objects.count() == 1, "Test object cannot be created"

    def test_update_model_without_versioning(self):
        self.tax.name = 'Food Tax (edited)'
        self.tax.save()

        assert Tax.objects.count() == 1, ("Changing a field that is not marked as `versioned` shouldn't "
                                          "generate a new revision")

    def test_update_model_with_versioning(self):
        self.tax.percentage_value = 13.5
        self.tax.save()

        assert Tax.objects.count() == 2, "Changing a field marked as `versioned` should generate a new revision"
