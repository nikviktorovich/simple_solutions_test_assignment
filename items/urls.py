from django.urls import path

from items import views


urlpatterns = [
    path('item/<int:pk>/', view=views.ItemDetailView.as_view(), name='item_detail'),
    path('item/<int:pk>', view=views.AddItemToOrderView.as_view(), name='add_to_order'),
    path('order/', view=views.OrderDetailView.as_view(), name='order_detail'),
]
