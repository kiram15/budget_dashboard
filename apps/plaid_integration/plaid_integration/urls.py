from django.urls import path

from . import views

app_name = "plaid_integration"

urlpatterns = [
    path("link/", views.link_page, name="link_page"),
    path("link/exchange/", views.exchange_token, name="exchange_token"),
    path("sync/<str:item_id>/", views.sync_now, name="sync_now"),
]
