from django.urls import path
from . import views
urlpatterns = [
    path('homeownerdash/', views.homeownerdash, name='homeownerdash'),
    path('homeowner_logout/',views.homeowner_logout,name='homeowner_logout'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('homeownerprofile/', views.homeownerprofile, name='homeownerprofile'),
    path('homeowneredit/', views.homeowneredit, name='homeowneredit'),
    path('addproject/',views.addproject, name='addproject'),
    path('homeownerviewprojects/', views.homeownerviewprojects, name='homeownerviewprojects'),
    path('homeownerviewapplications/<id>',views.homeownerviewapplications,name='homeownerviewapplications'),
    path('rejectedapp/<id>', views.rejectapp, name='rejectedapp'),
    path('approveapp/<id>', views.approveapp,name='approveapp'),
    path('runningprojects/', views.runningprojects, name='runningprojects'),
    path('viewupdates/<id>', views.viewupdates, name='viewupdates'),
    path('homeownercompletedprojects/', views.homeownercompletedprojects, name='homeownercompletedprojects'),
]