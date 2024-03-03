from django.test import TransactionTestCase

from payments.models import Payment
from products.models import Product
from taxes.models import Tax


class TestModelGetsVersioned(TransactionTestCase):
    def __init__(self, *args, **kwargs):
        self.tax = None
        super(TestModelGetsVersioned, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.tax = Tax.objects.create(
            name='Food Tax',
            percentage_value=12.4
        )

    def test_persisted_field_is_populated(self):
        tax = Tax.objects.get(id=self.tax.id)

        assert tax._persisted_id is not None, "Persistent field is None"
        assert tax._persisted_id == tax.id, "Tax._persisted_id should be equal to Tax.id if Tax has not been changed"

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

    def test_models_refer_to_correct_version(self):
        tax = Tax.objects.get(id=self.tax.id)

        payment = Payment.objects.create(
            amount=65000,
            tax=tax
        )

        product = Product.objects.create(
            name='Pasta alla Carbonara',
            price=800,
            tax=tax
        )

        self.tax.percentage_value = 13.5
        self.tax.save()

        # Reload payment
        payment = Payment.objects.get(id=payment.id)

        # Reload product
        product = Product.objects.get(id=product.id)

        assert int(payment.tax.percentage_value * 100) == 1240, "Payment should refer to the original model"
        assert int(product.tax.percentage_value * 100) == 1350, "Product should refer to the new model"

        tax = Tax.objects.get(id=self.tax.id)

        payment2 = Payment.objects.create(
            amount=65000,
            tax=tax
        )

        product2 = Product.objects.create(
            name='Pasta alla Carbonara',
            price=800,
            tax=tax
        )

        self.tax.percentage_value = 16.1
        self.tax.save()

        tax = Tax.objects.get(id=self.tax.id)

        payment3 = Payment.objects.create(
            amount=65000,
            tax=tax
        )

        # Reload items
        payment = Payment.objects.get(id=payment.id)
        product = Product.objects.get(id=product.id)
        payment2 = Payment.objects.get(id=payment2.id)
        product2 = Product.objects.get(id=product2.id)
        payment3 = Payment.objects.get(id=payment3.id)

        assert int(payment.tax.percentage_value * 100) == 1240, "Payment1 should refer to the original model"
        assert int(product.tax.percentage_value * 100) == 1610, "Product1 should refer to the new model"
        assert int(payment2.tax.percentage_value * 100) == 1350, "Payment2 should refer to the previous model"
        assert int(product2.tax.percentage_value * 100) == 1610, "Product2 should refer to the new model"
        assert int(payment3.tax.percentage_value * 100) == 1610, "Payment3 should refer to the new model"
