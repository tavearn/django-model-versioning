from django.test import TestCase

from payments.models import Payment
from products.models import Product
from taxes.models import Tax


class TestSampleApplication(TestCase):
    def setUp(self):
        tax = Tax.objects.create(
            name='Food Tax',
            percentage_value=12.4
        )

        Payment.objects.create(
            amount=65000,
            tax=tax
        )

        Product.objects.create(
            name='Pasta alla Carbonara',
            price=800,
            tax=tax
        )

    def test_data_exists(self):
        assert Tax.objects.all().count() > 0, "Tax object was not created"
        assert Payment.objects.all().count() > 0, "Payment object was not created"
        assert Product.objects.all().count() > 0, "Product object was not created"

    def test_models_relations(self):
        tax = Tax.objects.all().first()
        product = Product.objects.all().first()
        payment = Payment.objects.all().first()

        assert product.tax == tax, "`Product` was not linked to `Tax` correctly"
        assert payment.tax == tax, "`Payment` was not linked to `Tax` correctly"
