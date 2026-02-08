import pandas as pd
import gspread
from django.shortcuts import render 
from google.oauth2.service_account import Credentials
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Campaign
from .forms import CampaignForm
from django.conf import settings
from django.shortcuts import get_object_or_404



GS_SPREADSHEET_ID = "1uObBPhTJJCQYJwLH3e_60dYGMPeNTL4clu6P0L7ccNM"
RAWINPUTS_SPREADSHEET_ID = "1uObBPhTJJCQYJwLH3e_60dYGMPeNTL4clu6P0L7ccNM"

GS_SHEET_NAME = "Sheet1"
RAWINPUTS_SHEET_NAME = "RawInputs"

RAWINPUTS_COLUMN_MAP = {
    "tenant_id": "user_id",
    "rule_number": "Rule_ID",
    "week": "Week",
    "activation_base": "Trigger_Type",
    "comparison_type": "Trigger_Operator",
    "comparison_value": "Trigger_Value",
    "value_unit": "Trigger_Unit",
    "gender": "Gender",
    "skin_type": "Skin_Type",
    "hair_type": "Hair_Type",
    "priority" : "Priority",
    "product_source": "Product_Source",
    "is_active": "Active (Y/N)",
    "message_pattern" : "Message_Template"
}


class CampaignCreateViewWIthSheet(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    success_url = reverse_lazy("campaign-list")

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.tenant_id = self.request.user.id
        campaign.save()

        try:
            credentials = Credentials.from_service_account_info(
                settings.GOOGLE_SERVICE_ACCOUNT_INFO,
                scopes=[
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive",
                 ],
            )
            client = gspread.authorize(credentials)

            # ===============================
            # 1️⃣ Send Excel to Sheet1 (if uploaded)
            # ===============================
            if campaign.customers_file:
                df = pd.read_excel(campaign.customers_file.path)
                values = df.fillna("").astype(str).values.tolist()
                sheet1 = client.open_by_key(GS_SPREADSHEET_ID).worksheet(GS_SHEET_NAME)
                sheet1.append_rows(values, value_input_option="RAW")

            # ===============================
            # 2️⃣ Send Campaign fields to RawInputs
            # ===============================
            sheet2 = client.open_by_key(RAWINPUTS_SPREADSHEET_ID).worksheet(RAWINPUTS_SHEET_NAME)
            headers = sheet2.row_values(1)

            row = []
            for header in headers:
                model_field = next(
                    (k for k, v in RAWINPUTS_COLUMN_MAP.items() if v == header),
                    None
                )
                value = getattr(campaign, model_field, "") if model_field else ""
                row.append(str(value))

            sheet2.append_row(row, value_input_option="USER_ENTERED")

            messages.success(self.request, "Sent to Google Sheets successfully.")

        except Exception as e:
            messages.error(self.request, f"Google Sheets error: {e}")

        return super().form_valid(form)



# core/views.py
class CampaignListView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = "campaigns/campaign_list.html"
    context_object_name = "campaigns"

    def get_queryset(self):
        # Filter by tenant_id instead of user
        return Campaign.objects.filter(tenant_id=self.request.user.id).order_by(
            "-created_at"
        )


class CampaignDetailView(LoginRequiredMixin, DetailView):
    model = Campaign
    template_name = "campaigns/campaign_detail.html"

    def get_object(self):
        return get_object_or_404(
            Campaign, pk=self.kwargs["pk"], tenant_id=self.request.user.id
        )


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    success_url = reverse_lazy("campaign-list")

    def get_object(self):
        return get_object_or_404(
            Campaign, pk=self.kwargs["pk"], tenant_id=self.request.user.id
        )


class CampaignDeleteView(LoginRequiredMixin, DeleteView):
    model = Campaign
    template_name = "campaigns/campaign_confirm_delete.html"
    success_url = reverse_lazy("campaign-list")

    def get_object(self):
        return get_object_or_404(
            Campaign, pk=self.kwargs["pk"], tenant_id=self.request.user.id
        )

def DashBoardView(request):
    return render(request, 'campaigns/dashboard.html' , {})