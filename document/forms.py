from django import forms
from django.core.exceptions import ValidationError
from .models import db_docs
from bson import ObjectId


class ObjectIDField(forms.CharField):
    def __init__(self, *, **kwargs):
        super().__init__(min_length=24,
                         max_length=24,
                         empty_value='',
                         **kwargs)

    def prepare_value(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        if not isinstance(value, ObjectId):
            try:
                value = ObjectId(value)
            except ValueError:
                raise ValidationError(self.error_messages['invalid'],
                                      code='invalid')
        return value


class DocumentForm(forms.Form):
    _id = forms.ObjectIDField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def clean(self):
        pass

    def save(self):
        pass
