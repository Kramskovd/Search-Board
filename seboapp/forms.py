from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .apps import user_registered

from .models import Product, AdvUser


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {'user': forms.HiddenInput}


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(label='Адрес электронной почты')
    username = forms.CharField(label='Имя пользователя')
    first_name = forms.CharField(label='Ваше имя')
    last_name = forms.CharField(label='Фамилия')


    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name')


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Логин')
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput, required=False
                                )
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput,
                                )

    def clean_password(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)

        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password2 != password1:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')