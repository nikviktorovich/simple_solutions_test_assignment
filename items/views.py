from typing import Any
from typing import Dict

import django.db.models
from django.conf import settings
from django.http import response
from django.urls import reverse
from django.views import generic

from items import models


class ItemDetailView(generic.DetailView):
    model = models.Item
    template_name = 'item_detail.html'


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data['stripe_publishable_api_key'] = settings.STRIPE_PUBLISHABLE_API_KEY
        return context_data


class OrderDetailView(generic.DetailView):
    model = models.Order
    template_name = 'order_detail.html'


    def get_object(
        self,
        queryset: django.db.models.QuerySet[models.Order] | None = None,
    ) -> models.Order:
        if queryset is None:
            queryset = self.get_queryset()
        
        if 'order_id' in self.request.session:
            order_id = self.request.session['order_id']
            order, _ = queryset.get_or_create(pk=order_id)
        else:
            order = queryset.create()
            self.request.session['order_id'] = order.pk

        return order
    

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        order = self.get_object()
        items = models.Item.objects.filter(order_items__order=order).all()
        context_data = super().get_context_data(**kwargs)
        context_data['items'] = items
        context_data['stripe_publishable_api_key'] = settings.STRIPE_PUBLISHABLE_API_KEY
        return context_data


class AddItemToOrderView(generic.detail.SingleObjectMixin, generic.View):
    model = models.Item


    def post(self, request, *args, **kwargs):
        item = self.get_object()
        self.add_item_to_order(item) # type: ignore
        item_url = reverse('item_detail', kwargs={'pk': item.pk})
        return response.HttpResponseRedirect(item_url)
    

    def add_item_to_order(self, item: models.Item) -> None:
        order = self.get_order()
        order_item = models.OrderItem.objects.create(
            order=order,
            item=item,
        )
        order.order_items.add(order_item) # type: ignore
        order.save()
    

    def get_order(self) -> models.Order:
        queryset = models.Order.objects.all()
        
        if 'order_id' in self.request.session:
            order_id = self.request.session['order_id']
            order, _ = queryset.get_or_create(pk=order_id)
        else:
            order = queryset.create()
            self.request.session['order_id'] = order.pk

        return order
