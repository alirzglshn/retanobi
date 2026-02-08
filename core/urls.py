from django.urls import path
from .views import  CampaignListView , CampaignDetailView , CampaignUpdateView , CampaignDeleteView , CampaignCreateViewWIthSheet , DashBoardView

urlpatterns = [
    path("", DashBoardView , name="dashboard-view"),
    path("campaigns/", CampaignListView.as_view(), name="campaign-list"),
    path("campaigns/create/", CampaignCreateViewWIthSheet.as_view(), name="campaign-create"),
    path("campaigns/<int:pk>/", CampaignDetailView.as_view(), name="campaign-detail"),
    path("campaigns/<int:pk>/edit/", CampaignUpdateView.as_view(), name="campaign-update"),
    path("campaigns/<int:pk>/delete/", CampaignDeleteView.as_view(), name="campaign-delete"),
]
