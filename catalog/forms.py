import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    # в форме задаём поля, которые будут под ввод
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3)")

    # валидация значения - метод clean_<fieldname>()
    def clean_renewal_date(self):
        # берем значение
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past
        # _ - нужно, если мы захотим в дальнейшем делать нашему сайту перевод на другие языки
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))

        # Check if a date is in the allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

        # Remember to always return the cleaned data
        return data
