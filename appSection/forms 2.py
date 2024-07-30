from django import forms
from appCategory.models import Category
from .models import Section
from django.forms import inlineformset_factory


class SectionForm(forms.ModelForm):
    # categories = forms.ModelMultipleChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )

    class Meta:
        model = Section
        fields = ['name', 'description']

# SectionFormSet = inlineformset_factory(Category, Section, form=SectionForm, extra=1, can_delete=True)