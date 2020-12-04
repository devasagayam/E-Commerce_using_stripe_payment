from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from . import models
from django.forms import ModelForm, Textarea


"""class refund_accept(ModelForm):
    class Meta:
    model = models.Refund
    fields = ['reason', 'email']
    widgets = {

        'reason': forms.Textarea(attrs={'disabled': True}),
        'email': forms.Textarea(attrs={'disabled': True}),

    }"""


class addform(forms.ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['slug']
        model = models.Item
        widgets = {
          'description': Textarea(attrs={'rows':4, 'cols':40}),
        }



PAYMENT_CHOICES = (
    ('S', 'Creddit/Debit Card'),
    ('P', 'UPI')
)

"""
class profileform(forms.ModelForm):
    class Meta:
        fields=('Full_Name','Gender','Phone_Number','photo')
        model=models.UserProfile

"""

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
