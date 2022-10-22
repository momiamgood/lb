from django.contrib import admin
from .models import User
from .models import Order


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'fio',
                    'email',)
    fields = ['username', 'fio', 'email']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_name',
        'disc',
        'date_joined',
        'status',
        'category',
        'order_img',
        'orderer'
    )
    fields = ['order_name', 'disc', 'date_joined', 'category', 'status', 'order_img', 'orderer']
