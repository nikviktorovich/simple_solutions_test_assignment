import decimal

from django.test import TestCase
from django.urls import reverse

import items.models


class TestPaymentsBuy(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.item = items.models.Item.objects.create(
            name='Some item',
            description='Some description',
            price=decimal.Decimal('100.00')
        )
    

    def test_payments_buy_response_code_ok(self) -> None:
        response = self.client.get(reverse('payment_buy', kwargs={
            'pk': self.item.pk,
        }))
        self.assertEqual(response.status_code, 200)
