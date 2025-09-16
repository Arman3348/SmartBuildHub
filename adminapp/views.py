from django.shortcuts import render,redirect
from django.contrib import messages
from homeownerapp.models import *
from mainapp.models import *
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid = request.session['adminid']
    context = {
        'adminid': adminid,
        'th': UserLogin.objects.filter(usertype='homeowner').count(),
        'tc': UserLogin.objects.filter(usertype='contractor').count(),
        'tp': Project.objects.count(),
        'cp': Project.objects.filter(status='Completed').count(),
        'op': Project.objects.filter(status='under_construction').count(),
        'te': Enquiry.objects.count(),
    }
    return render(request, 'admindash.html', context)

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, "You have been logged out successfully.")
        return redirect('adminlogin')
    else:
        return redirect('index')

# Change Password View
@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def admin_change_password(request):
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            admin = LoginInfo.objects.get(username=adminid)
            if admin.password != old_password:
                messages.error(request, "Old password is incorrect.")
                return redirect('admin_change_password')
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect('admin_change_password')
            elif new_password == old_password:
                messages.error(request, "New passwords is same as old password.")
                return redirect('admin_change_password')
            else:
                admin.password = new_password
                admin.save()
                messages.success(request, "Password changed successfully.")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, "User not found.")
    return render(request, 'admin_change_password.html', {'adminid': adminid})

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def admin_enquiries(request):
    if not request.session.get('adminid'):
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid = request.session['adminid']
    enquiries = Enquiry.objects.all().order_by('-enqdate')
    return render(request, 'admin_enquiries.html', {'enquiries': enquiries, 'adminid': adminid})

# Delete Enquiry
@cache_control(no_cache = True,must_revalidate=True,no_store=True )
@csrf_exempt
def admin_delete_enquiry(request, enq_id):
    if request.method == 'POST' and request.session.get('adminid'):
        try:
            enq = Enquiry.objects.get(id=enq_id)
            enq.delete()
            messages.success(request, 'Enquiry deleted successfully.')
        except Enquiry.DoesNotExist:
            messages.error(request, 'Enquiry not found.')
    return redirect('admin_enquiries')
@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def managehomeowners(request):
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid = request.session['adminid']
    homeowners = UserLogin.objects.filter(usertype='homeowner')
    return render(request, 'managehomeowners.html', {'adminid': adminid, 'homeowners': homeowners})
@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def managecontractors(request):
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid = request.session['adminid']
    contractors = UserLogin.objects.filter(usertype='contractor')
    return render(request, 'managecontractors.html', {'adminid': adminid, 'contractors': contractors})

