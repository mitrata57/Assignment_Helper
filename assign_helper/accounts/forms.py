from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    # Confirm password is built into UserCreationForm, 
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone")
        widgets = {
            'phone': forms.TextInput(attrs={'type': 'tel'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None 
            field.widget.attrs['class'] = (
                'w-full px-4 py-2 rounded-lg border-2 border-slate-200 ' 
                'bg-white text-slate-700 focus:border-blue-400 focus:outline-none transition'
            )