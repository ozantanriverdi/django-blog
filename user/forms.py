'''Import form module of Django'''
from django import forms


class LoginForm(forms.Form):
    '''User Login Form'''
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    '''Inherit from Form class under forms module'''

    username = forms.CharField(max_length=50, label="Username")
    password = forms.CharField(max_length=20, label="Password",
                               widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Confirm Password",
                              widget=forms.PasswordInput)

    def clean(self):
        # Implement a clean() method on your Form when you must add custom
        # validation for fields that are interdependent.
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            # password and confirm both filled and are not the same
            raise forms.ValidationError("Passwords don't match")

        values = {
            "username": username,
            "password": password
        }
        return values
