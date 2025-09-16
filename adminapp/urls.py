from django.urls import path
from . import views

urlpatterns = [
    path('admin_change_password/',views.admin_change_password, name='admin_change_password'),

]