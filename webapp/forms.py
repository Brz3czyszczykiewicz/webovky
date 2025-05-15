from pyclbr import Class

from django import forms

from webapp.models import Customer, Trip


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

        labels = {
            "customer_first_name": "Jméno",
            "customer_last_name": "Příjmení",
            "customer_email": "Email",
            "customer_phone": "Telefonní číslo",
        }

        placeholder = {
            "customer_first_name": "haha"
        }

        help_texts = {
            "customer_email": "Je nutné zadat buď telefon, nebo email"
        }

        widgets = {
            "customer_first_name": forms.TextInput(attrs={'class': 'form-control'}),

        }


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = "__all__"

        labels = {
            "start_time": "Od",
            "end_time": "Do",
        }

        help_texts = {}

        widgets = {
            "start_time": forms.DateInput(attrs={'class': 'form-control', "type":"date"}),
            "end_time": forms.DateInput(attrs={'class': 'form-control', "type":"date"}),
        }