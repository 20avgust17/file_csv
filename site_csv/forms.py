from django import forms

from site_csv.models import Schema, Column, CSVData


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        exclude = ['modified']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'columns': forms.HiddenInput(),
            'separator': forms.Select(attrs={'class': 'form-control'}),
            'string_character': forms.Select(attrs={'class': 'form-control'}),
        }


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = '__all__'


class CSVDataForms(forms.ModelForm):
    class Meta:
        model = CSVData
        fields = ["rows"]
