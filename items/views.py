from typing import Any
from typing import Dict

from django.conf import settings
from django.views import generic

from items import models


class ItemDetailView(generic.DetailView):
    model = models.Item
    template_name = 'item_detail.html'


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data['stripe_publishable_api_key'] = settings.STRIPE_PUBLISHABLE_API_KEY
        return context_data
