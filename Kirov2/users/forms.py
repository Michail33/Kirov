from django import forms
from .validator import russian_email
from django.core.validators import MinLengthValidator

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           validators=[MinLengthValidator(2)], initial='Name123')
    email = forms.EmailField(validators=[russian_email])
    message = forms.CharField(widget=forms.Textarea)
    demo = forms.BooleanField(required=False, help_text='Text Help me', label='Статус', initial=None)

