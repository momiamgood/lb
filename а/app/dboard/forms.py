from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User, Order, AdditionalImage
from django.forms import inlineformset_factory


class UserRegistration(UserCreationForm):
    error_messages = {
        'password_mismatch': _("Пароли не совпадают"),
    }
    fio = forms.CharField(label='ФИО')
    email = forms.EmailField(label='Адрес электронной почты')
    password1 = forms.CharField(label=_("Пароль"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Подтверждение пароля"),
                                widget=forms.PasswordInput,)
    agreement = forms.BooleanField(label='Согласие на обработку персональных данных', widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ('username', 'fio', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


AIFormSet = inlineformset_factory(Order, AdditionalImage, fields='__all__')


class OrderCreationForm(forms.Form):
    order_name = forms.CharField(label='Название заказа')
    disc = forms.CharField(widget=forms.Textarea, help_text='Описание заказа')
    CHOICES = (
        ('2D', '2D-design'),
        ('3D', '3D-design'),
        ('Web', 'Web-design'),
        ('Mobile', 'Mobile-design'),
    )
    category = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    order_img = forms.ImageField(label='Изображение', required=False)

    class Meta:
        model = Order
        fields = ('order_name', 'disc', 'category', 'order_img')

