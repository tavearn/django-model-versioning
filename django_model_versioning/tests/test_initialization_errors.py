from django.db.models import Model
from django.test import TestCase

from lib.versioned_model import VersionedModel


class TestInitializationErrors(TestCase):
    def test_versioned_model_throws_error_if_only_parent(self):
        has_error = False
        try:
            class MyModel(VersionedModel):
                class Meta:
                    app_label = 'lib'

                pass
        except TypeError:
            has_error = True

        assert has_error, "VersionedModel should throw an exception if it is the only base class"

    def test_versioned_model_throws_error_withot_model(self):
        class SampleBaseClass:
            pass

        has_error = False

        try:
            class MyModel(VersionedModel, SampleBaseClass):
                class Meta:
                    app_label = 'lib'

                pass
        except TypeError:
            has_error = True

        assert has_error, "VersionedModel should throw an exception if it is implemented without Model class"

    def test_versioned_model_should_work_if_inherits_from_model(self):
        has_error = False

        try:
            class MyModel(VersionedModel, Model):
                class Meta:
                    app_label = 'lib'

                pass
        except TypeError:
            has_error = True

        assert not has_error, "VersionedModel should work if the class also inherits from model"
