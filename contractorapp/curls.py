from django.urls import path
from . import views

urlpatterns = [
    path('contractordash/', views.contractordash, name='contractordash'),
    path('changepassword/', views.contractorchangepassword, name='contractorchangepassword'),
    path('logout/', views.contractor_logout, name='contractor_logout'),
    path('contractorprofile/',views.contractorprofile,name='contractorprofile'),
    path('contractoredit/',views.contractoredit,name='contractoredit'),
    path('contractorviewprojects/', views.contractorviewprojects, name='contractorviewprojects'),
    path('applyproject/<id>', views.applyproject, name='applyproject'),
    path('contractorapplications/', views.contractorapplications, name='contractorapplications'),
    path('assignedprojects/',views.assignedprojects,name='assignedprojects'),
    path('addprogress/<id>', views.addprogress, name='addprogress'),
]