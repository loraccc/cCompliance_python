from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm 
from django.contrib.auth.models import Permission
from django.forms import inlineformset_factory

from .models import CustomUser, Role ,Category


class CustomUserCreationForm(UserCreationForm):
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'roles']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'permissions']

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissions",
        help_text="Select permissions for the role."
    )
class CustomUserChangeForm(UserChangeForm):
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'roles']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'sections': forms.CheckboxSelectMultiple(),
        }
