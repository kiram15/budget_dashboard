from django.urls import path

from . import views

app_name = "investments"

urlpatterns = [
    path("holdings/", views.HoldingListView.as_view(), name="holding_list"),
    path(
        "portfolio-history/",
        views.PortfolioHistoryView.as_view(),
        name="portfolio_history",
    ),
]
