from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'rounded-input'}),
        min_length=8,
        label=''
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль', 'class': 'rounded-input'}),
        min_length=8,
        label=''
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']
        help_texts = {'username': None}
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'rounded-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'rounded-input'}),
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'class': 'rounded-input'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'username': '',
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control rounded-input'})  # Добавляем общий класс ко всем полям

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Пароли не совпадают")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Хешируем пароль
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'class': 'rounded-input'}),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'rounded-input'}),
        min_length=8,
        label = ''
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control rounded-input'})