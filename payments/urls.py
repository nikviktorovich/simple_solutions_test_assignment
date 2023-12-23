from django.urls import path

from payments import views


urlpatterns = [
    path('buy/<int:pk>/', view=views.PaymentDetailAPIView.as_view(), name='payment_buy'),
]
