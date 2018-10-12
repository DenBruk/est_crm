from django import forms
from .models import data,company,services
class dataForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=company.objects.order_by('company_name'))
    service = forms.ModelChoiceField(queryset=services.objects.order_by('service_name'))
    class Meta:
        model = data
        fields = ('company',
                  'service',
                  'date_of_exp',
                  'qty'
        )
        widgets = {'date_of_exp': forms.DateInput(attrs={'class':'datepicker'}),
        }
