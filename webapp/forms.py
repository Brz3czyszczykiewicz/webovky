from pyclbr import Class

from django import forms

from webapp.models import Customer, Trip


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ["customer_trip"]




        labels = {
            "customer_first_name": "Jméno",
            "customer_last_name": "Příjmení",
            "customer_email": "Email",
            "customer_phone": "Telefonní číslo",
            "customer_count": "Počet osob",
            "customer_message": "Krátká poznámka"

        }

        placeholder = {
            "customer_first_name": "haha"
        }

        help_texts = {
            "customer_email": "Je nutné zadat buď telefon, nebo email"
        }

        widgets = {
            "customer_first_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            "customer_last_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            "customer_email": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            "customer_phone": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            "customer_count": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kolik Vás bude? :)'}),
            "customer_message": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nepovinné'}),


        }
    def clean(self):
        cleaned_data = super().clean()
        customer_email = cleaned_data.get("customer_email")
        customer_phone = cleaned_data.get("customer_phone")
        if not customer_email and not customer_phone:
            raise forms.ValidationError("Je nutné zadat buď telefon, nebo email")
        return cleaned_data

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