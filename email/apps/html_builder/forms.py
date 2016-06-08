from django.forms import forms

class BlacklistForm(forms.Form):
    email = forms.CharField(label='Email', required=True, widget=forms.TextInput(attrs={'type':'email', 'class':'form-control', 'placeholder':'nombre@email.com'}))
    country = forms.ChoiceField(label='País', choices=COUNTRIES, required=True, widget=forms.Select(attrs={'class':'form-control'}))