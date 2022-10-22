from django.urls import path, include
from .views import Registration, OrderCreate, profile_delete
from . import views
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', Registration.as_view(), name='registration'),
    path('', views.user_orders_count, name='user_orders_count'),
    path('my-account/', views.user_orders_count, name='my-account'),
    path('order-creation/', OrderCreate.as_view(), name='order-creation'),
    path('delete-account', profile_delete, name='profile_delete')
]
