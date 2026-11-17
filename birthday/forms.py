from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Birthday

BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}
RECIPIENTS = ['admin@example.com', 'manager@example.com', 'support@example.com']


class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        exclude = ('author',) 
        
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]

    def clean(self):
        cleaned_data = super().clean()
        
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if f'{first_name} {last_name}' in BEATLES:
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, своё настоящее имя!'
            )
        
        return cleaned_data