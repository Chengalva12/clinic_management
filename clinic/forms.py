from django import forms
from .models import Patient

class AssignPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['doctor']
        widgets = {
            'doctor': forms.HiddenInput(),  # Hide this field if auto-assigning to the current doctor
        }
