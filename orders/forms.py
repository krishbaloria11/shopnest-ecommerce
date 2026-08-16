from django import forms
from .models import PAYMENT_METHOD_CHOICES


class CheckoutForm(forms.Form):
    """Form for collecting shipping and demo payment preferences at checkout."""
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g. Alex Johnson', 'required': 'required',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g. alex.johnson@example.com', 'required': 'required',
    }))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g. +91 98765 43210', 'required': 'required',
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'House / Flat No., Street, Landmark, Area', 'rows': 3, 'required': 'required',
    }))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g. Bengaluru / Mumbai / Delhi', 'required': 'required',
    }))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g. Karnataka / Maharashtra', 'required': 'required',
    }))
    zip_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g. 560001', 'required': 'required',
    }))
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        initial='card',
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'}),
        required=False
    )
