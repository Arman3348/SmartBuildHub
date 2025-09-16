from django.urls import path
from . import views
urlpatterns = [
    path('admindash/', views.admindash, name='admindash'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('change-password/', views.admin_change_password, name='admin_change_password'),
    path('enquiries/', views.admin_enquiries, name='admin_enquiries'),
    path('enquiries/delete/<int:enq_id>/', views.admin_delete_enquiry, name='admin_delete_enquiry'),
    path('managehomeowners/', views.managehomeowners, name='managehomeowners'),
    path('managecontractors/',views.managecontractors,name='managecontractors'),
]