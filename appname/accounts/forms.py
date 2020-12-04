from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts import models
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth import get_user_model

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        exclude = ['status','user']
        widgets = {
            'DOB': DatePickerInput(), # default date-format %m/%d/%Y will be used
            'gender':forms.RadioSelect(),

        }



class SignupForm(UserCreationForm):

    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "User Name"
        self.fields["email"].label = "Email address"
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
