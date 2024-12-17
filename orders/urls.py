from django.urls import path

from orders.views import OrderSingleView


urlpatterns = [
    path("", OrderSingleView.as_view()),
]
