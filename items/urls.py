from django.urls import path

from items import views


urlpatterns = [
    path('<int:pk>/', view=views.ItemDetailView.as_view(), name='item_detail'),
]
