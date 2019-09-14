from django import forms


class RenewBookForm(forms.BaseForm):
    renewal_date = forms.DateField(help_text="Enter a date between noew and 4 weeks (default 3)")
