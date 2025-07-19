from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("payment/<uuid:order_id>/", views.initiate_payment, name="initiate_payment"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path("success/<uuid:order_id>/", views.order_success, name="order_success"),
    path("list/", views.order_list, name="order_list"),
    path("detail/<uuid:order_id>/", views.order_detail, name="order_detail"),
]
