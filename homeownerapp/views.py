from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .forms import ProjectForm
from homeownerapp.models import *
from contractorapp.models import *
from django.utils import timezone


def homeownerdash(request):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    context = {
        'homeowner': homeowner,
        'name': homeowner.name,
        'email': homeowner.email,
        'profile':homeowner.picture,
        'tp': Project.objects.count(),
        'cp': Project.objects.filter(status='Completed').count(),
        'op': Project.objects.filter(status='Ongoing').count(),
        
    }
    return render(request, 'homeownerdash.html', context)

def homeowner_logout(request):
    if 'homeownerid' in request.session:
        del request.session['homeownerid']
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')
    else:
        return redirect('index')
    
def changepassword(request):
    if 'homeownerid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            log=LoginInfo.objects.get(username=homeownerid)
            homeowner = UserLogin.objects.get(email=homeownerid)
            if log.password != old_password:
                messages.error(request, "Old password is incorrect.")
                return redirect('changepassword')
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect('changepassword')
            elif new_password == old_password:
                messages.error(request, "New password is same as old password.")
                return redirect('changepassword')
            else:
                log.password=new_password
                homeowner.password = new_password
                log.save()
                homeowner.save()
                messages.success(request, "Password changed successfully.")
                return redirect('homeownerdash')
        except UserLogin.DoesNotExist:
            messages.error(request, "User not found.")
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    context = {
        'homeowner': homeowner,
        'name': homeowner.name,
        'email': homeowner.email,
        'profile':homeowner.picture,
        }        
    return render(request, 'changepassword.html',context)

def homeownerprofile(request):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'email':homeowner.email,
        'contact':homeowner.mobile,
        'bio':homeowner.bio,
        'address':homeowner.address,
        'profile':homeowner.picture,

    }
    return render(request, 'homeownerprofile.html',context)

def homeowneredit(request):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'email':homeowner.email,
        'contact':homeowner.mobile,
        'bio':homeowner.bio,
        'address':homeowner.address,
        'profile':homeowner.picture,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        bio= request.POST.get('bio')
        profile= request.FILES.get('profile')
        homeowner.name=name
        homeowner.mobile=phone
        homeowner.address=address
        homeowner.bio=bio
        if profile:
            homeowner.picture = profile            
        homeowner.save()  
        messages.success(request, "Profile updated successfully.")
        return redirect('homeownerprofile')
    return render(request, 'homeowneredit.html', context)

def addproject(request):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    form = ProjectForm()
    context = {
        'homeowner': homeowner,
        'name': homeowner.name,
        'email': homeowner.email,
        'profile':homeowner.picture,
        'form': form
    }
    if request.method=="POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.homeowner = homeowner 
            project.save()
            messages.success(request, "Project added successfully.")
            return redirect('homeownerdash')
        else:
            messages.error(request, "Please check the form, form incompleted")
            return redirect('addproject')
    return render(request, 'addproject.html', context)

def homeownerviewprojects(request):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    Projects = Project.objects.filter(homeowner=homeowner)
    context = {
        'homeowner': homeowner,
        'name': homeowner.name,
        'email': homeowner.email,
        'profile':homeowner.picture,
        'Projects': Projects,
    }
    return render(request,'homeownerviewprojects.html',context)

def homeownerviewapplications(request,id):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    Projects = Project.objects.get(id=id)
    applications = ContractorApplication.objects.filter(project=Projects)
    context = {
        'homeowner': homeowner,
        'name': homeowner.name,
        'email': homeowner.email,
        'profile':homeowner.picture,
        'project':Projects,
        'applications': applications
    }
    return render(request, 'homeownerviewapplications.html', context)


def rejectapp(request,id):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    app = ContractorApplication.objects.get(id=id)
    app.status = 'rejected'
    app.save()
    messages.success(request, "Application rejected successfully.")
    return redirect('homeownerviewapplications', id=app.project.id)


def approveapp(request,id):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    app = ContractorApplication.objects.get(id=id)
    project = Project.objects.get(id=app.project.id)
    apps = ContractorApplication.objects.filter(project=app.project).update(status='rejected')
    app.status = 'approved'
    app.save()
    project.contractor = app.contractor
    project.start_date = timezone.now()
    project.status = 'under_construction'
    project.save()
    messages.success(request, "Application approved successfully.")
    return redirect('homeownerviewapplications', id=app.project.id)


def runningprojects(request):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner, status='under_construction')
    context = {
        'homeowner': homeowner,
        'name': homeowner.name,
        'email': homeowner.email,
        'profile':homeowner.picture,
        'projects': projects,
    }
    return render(request, 'runningprojects.html', context)


def viewupdates(request, id):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    Projects = Project.objects.get(id=id)
    updates = ProgressUpdate.objects.filter(project=Projects)
    context = {
        'homeowner': homeowner,
        'name': homeowner.name,
        'email': homeowner.email,
        'profile':homeowner.picture,
        'project': Projects,
        'updates': updates
    }
    return render(request, 'viewupdates.html', context)


def homeownercompletedprojects(request):
    if 'homeownerid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserLogin.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner, status='completed')
    context = {
        'homeowner': homeowner,
        'name': homeowner.name,
        'email': homeowner.email,
        'profile':homeowner.picture,
        'projects': projects,
    }
    return render(request, 'homeownercompletedprojects.html', context)



