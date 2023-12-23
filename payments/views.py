import stripe
from django.conf import settings
from django.urls import reverse
from rest_framework import generics
from rest_framework import response

import items.models
from payments import models
from payments import serializers


class PaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = items.models.Item.objects.all()
    serializer_class = serializers.PaymentSerializer


    def retrieve(self, request, *args, **kwargs) -> response.Response:
        item = self.get_object()
        session = self.create_session(item=item)
        payment = models.Payment.objects.create(item=item, session_id=session.id)
        serializer = self.get_serializer(payment)
        return response.Response(data=serializer.data)
    

    def create_session(self, item: items.models.Item) -> stripe.checkout.Session:
        item_url = self.get_item_absolute_url(item)
        line_items = [
            self.create_line_item(item=item),
        ]
        return stripe.checkout.Session.create(
            api_key=settings.STRIPE_SECRET_API_KEY,
            line_items=line_items,
            success_url=item_url,
            cancel_url=item_url,
            mode='payment',
        )


    def get_item_absolute_url(self, item: items.models.Item) -> str:
        relative_item_url = reverse('item_detail', kwargs={'pk': item.pk})
        absolute_item_url = self.request.build_absolute_uri(relative_item_url)
        return absolute_item_url


    def create_line_item(
            self,
            item: items.models.Item,
        ) -> stripe.checkout.Session.CreateParamsLineItem:
        currency = settings.STRIPE_CURRENCY
        unit_amount = int(item.price * 100)
        product_data = {
            'name': item.name,
            'description': item.description,
        }
        price_data = stripe.checkout.Session.CreateParamsLineItemPriceData(
            currency=currency,
            unit_amount=unit_amount,
            product_data=product_data, # type: ignore
        )
        return stripe.checkout.Session.CreateParamsLineItem(
            price_data=price_data,
            quantity=1,
        )

