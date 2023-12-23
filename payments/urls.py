from django.urls import path

from payments import views


urlpatterns = [
    path('buy/<int:pk>/', view=views.PaymentDetailAPIView.as_view(), name='payment_buy'),
    path('buy_order/', view=views.PaymentOrderDetailAPIView.as_view(), name='payment_buy_order'),
]
