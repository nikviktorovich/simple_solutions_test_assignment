from typing import List

import stripe
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import response

import items.models
from payments import models
from payments import serializers


class PaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = items.models.Item.objects.all()
    serializer_class = serializers.PaymentSerializer


    @transaction.atomic
    def retrieve(self, request, *args, **kwargs) -> response.Response:
        order = self.create_order()
        session = self.create_session(order=order)
        payment = self.create_payment(order=order, session_id=session.id)
        serializer = self.get_serializer(payment)
        return response.Response(data=serializer.data)


    def create_order(self) -> items.models.Order:
        order = items.models.Order.objects.create()
        item = self.get_object()
        order_item = items.models.OrderItem.objects.create(
            order=order,
            item=item,
        )
        return order
    

    def create_payment(
        self,
        order: items.models.Order,
        session_id: str,
    ) -> models.Payment:
        return models.Payment.objects.create(order=order, session_id=session_id)


    def create_session(self, order: items.models.Order) -> stripe.checkout.Session:
        return_url = self.get_return_url()
        line_items = self.create_line_items(order=order)

        if not line_items:
            raise exceptions.APIException(detail='Order is empty', code=400)

        return stripe.checkout.Session.create(
            api_key=settings.STRIPE_SECRET_API_KEY,
            line_items=line_items,
            success_url=return_url,
            cancel_url=return_url,
            mode='payment',
        )
    

    def get_return_url(self) -> str:
        item = self.get_object()
        item_url = reverse_lazy('item_detail', item.pk)
        return self.request.build_absolute_uri(item_url)
    

    def create_line_items(
        self,
        order: items.models.Order,
    ) -> List[stripe.checkout.Session.CreateParamsLineItem]:
        order_items = order.order_items.all() # type: ignore
        line_items = [self.create_line_item(order_item.item) for order_item in order_items]
        return line_items


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


class PaymentOrderDetailAPIView(PaymentDetailAPIView):
    def create_order(self) -> items.models.Order:
        if 'order_id' not in self.request.session:
            order = items.models.Order.objects.create()
        else:
            order_id = self.request.session['order_id']
            order = get_object_or_404(items.models.Order, pk=order_id)
        
        return order


    def get_return_url(self) -> str:
        order_url = reverse_lazy('order_detail')
        return self.request.build_absolute_uri(order_url)
