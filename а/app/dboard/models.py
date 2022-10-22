from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from .utilities import get_timestamp_path


class User(AbstractUser):
    username = models.CharField('Логин', max_length=150,unique=True, validators=[
        RegexValidator(
            regex='^[A-Za-z -]*$',
            message='Имя пользователя содержит только латиницу',
            code='invalid_username'
        )]
    )
    fio = models.CharField('ФИО', max_length=150, validators=[
        RegexValidator(
            regex='^[А-Яа-я -]*$',
            message='Поле ФИО содержит только кириллицу',
            code='invalid_username'
        )]
    )
    email = models.EmailField('Email', max_length=150)

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


class Order(models.Model):
    orderer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_name = models.CharField('Название заявки', max_length=150, null=False)
    disc = models.TextField('Описание', max_length=300)

    CATEGORIES = (
        ('2D', '2D-design'),
        ('3D', '3D-design'),
        ('Web', 'Web-design'),
        ('Mobile', 'Mobile-design'),
    )
    date_joined = models.DateTimeField("Дата создания заявки", default=timezone.now)
    category = models.CharField(
        'Категория',
        max_length=6,
        choices=CATEGORIES,
        blank=True,
        default='Другое',
        help_text='Категория заказа')

    STATUS = (
        ('Новый', 'Новый'),
        ('В работе', 'В работе'),
        ('Выполнен', 'Выполнен'),
    )
    status = models.CharField(
        'Статус',
        max_length=8,
        choices=STATUS,
        blank=True,
        default='Новый',
        help_text='Категория заказа')

    order_img = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')

    def delete(self, *args, **kwargs):
        for ai in self.order_img_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.order_name


class AdditionalImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Объявление')
    order_img = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'
