# core/forms.py
from django import forms
from .models import Campaign


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign

        
        fields = [
            "name",
            "week",
            "activation_base",
            "comparison_type",
            "comparison_value",
            "value_unit",
            "customer_type",
            "priority",
            "gender",
            "skin_type",
            "hair_type",
            "product_source",
            "customers_file",
            "message_pattern",
            "is_active",
        ]

        labels = {
            "name": "نام کمپین",
            "week": "هفته",
            "activation_base": "مبنای فعال‌سازی",
            "comparison_type": "نوع مقایسه",
            "comparison_value": "مقدار مقایسه",
            "value_unit": "واحد مقدار",
            "priority" : "اولویت",
            "customer_type": "نوع مشتری",
            "gender": "جنسیت",
            "skin_type": "نوع پوست",
            "hair_type": "نوع مو",
            "product_source": "منبع محصول",
            "customers_file": "فایل مشتریان",
            "message_pattern": "الگوی پیام",
            "is_active": "فعال باشد",
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "مثلاً کمپین خرید مجدد"
            }),

            "week": forms.Select(attrs={"class": "form-control"}),
            "activation_base": forms.Select(attrs={"class": "form-control"}),
            "comparison_type": forms.Select(attrs={"class": "form-control"}),
            "comparison_value": forms.Select(attrs={"class": "form-control"}),
            "value_unit": forms.Select(attrs={"class": "form-control"}),
            "customer_type": forms.Select(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "skin_type": forms.Select(attrs={"class": "form-control"}),
            "hair_type": forms.Select(attrs={"class": "form-control"}),
            "product_source": forms.Select(attrs={"class": "form-control"}),
            "priority" : forms.Select(attrs={"class":"form-control"}),  

            "customers_file": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "message_pattern": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "متن پیام ارسالی به مشتری"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
