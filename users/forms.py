from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    group = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name="admin"),
        required=True,
        empty_label=None
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "group")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            group = self.cleaned_data["group"]
            user.groups.add(group)
        return user
    
class ProfileUpdateForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name="admin"),
        required=True,
        empty_label=None
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "group")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # update group
            group = self.cleaned_data["group"]
            # clear previous non-admin groups before reassigning
            user.groups.clear()
            user.groups.add(group)
        return user
    
class CustomPasswordChangeForm(PasswordChangeForm):
    """Optional customization if you want to style fields manually"""
    pass
