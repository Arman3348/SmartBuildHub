from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from mainapp.models import UserLogin
from homeownerapp.models import *
from .models import *
from decimal import Decimal

# Create your views here.
def contractordash(request):
    if 'contractorid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserLogin.objects.filter(email=contractorid).first()
    context = {
        'contractor': contractor,
        'name': contractor.name,
        'email': contractor.email,
        'profile':contractor.picture,
        'tp': Project.objects.count(),
        'cp': Project.objects.filter(status='Completed').count(),
        'op': Project.objects.filter(status='Ongoing').count(),
    }
    return render(request, 'contractordash.html', context)


def contractor_logout(request):
    if 'contractorid' in request.session:
        del request.session['contractorid']
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')
    else:
        return redirect('index')

def contractorchangepassword(request):
    if 'contractorid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            contractor = UserLogin.objects.get(email=contractorid)
            if contractor.password != old_password:
                messages.error(request, "Old password is incorrect.")
                return redirect('contractorchangepassword')
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect('contractorchangepassword')
            elif new_password == old_password:
                messages.error(request, "New password is same as old password.")
                return redirect('contractorchangepassword')
            else:
                contractor.password = new_password
                contractor.save()
                messages.success(request, "Password changed successfully.")
                return redirect('contractordash')
        except UserLogin.DoesNotExist:
            messages.error(request, "User not found.")
    contractor = UserLogin.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'email':contractor.email,
        'contact':contractor.mobile,
        'bio':contractor.bio,
        'address':contractor.address,
        'profile':contractor.picture,
    }
    return render(request, 'contractorchangepassword.html',context)

def contractorprofile(request):
    if 'contractorid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserLogin.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'email':contractor.email,
        'contact':contractor.mobile,
        'bio':contractor.bio,
        'address':contractor.address,
        'profile':contractor.picture,
    }
    return render(request, 'contractorprofile.html',context)

def contractoredit(request):
    if 'contractorid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserLogin.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'email':contractor.email,
        'contact':contractor.mobile,
        'bio':contractor.bio,
        'address':contractor.address,
        'profile':contractor.picture,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        bio= request.POST.get('bio')
        profile= request.FILES.get('profile')
        contractor.name=name
        contractor.mobile=phone
        contractor.address=address
        contractor.bio=bio
        if profile:
            contractor.picture = profile            
        contractor.save()  
        messages.success(request, "Profile updated successfully.")
        return redirect('contractorprofile')
    return render(request, 'contractoredit.html', context)

def contractorviewprojects(request):
    if 'contractorid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserLogin.objects.filter(email=contractorid).first()
    projects = Project.objects.filter(contractor=None)
    context = {
        'name': contractor.name,
        'email': contractor.email,
        'Projects': projects,
        'profile': contractor.picture,
    }
    return render(request, 'contractorviewprojects.html', context)

def applyproject(request,id):
    if 'contractorid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserLogin.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'contractor': contractor,
        'name': contractor.name,
        'email': contractor.email,
        'profile':contractor.picture,
        'project': project,
    }
    application = ContractorApplication.objects.filter(project=project, contractor=contractor)
    if application.exists():
        messages.error(request, "You have already applied for this project.")
        return redirect('contractorviewprojects')
    if request.method == "POST":
        proposal_text = request.POST.get('proposal_text')
        design_file = request.FILES.get('design_file')
        estimated_budget = request.POST.get('estimated_budget')
        try:
            estimated_budget = Decimal(estimated_budget)
        except:
            messages.error(request, "Invalid Estimated Budget.")
            return redirect('contractorviewprojects')
        estimated_duration = request.POST.get('estimated_duration')
        app = ContractorApplication(
            project=project,
            contractor=contractor,
            proposal_text=proposal_text,
            design_file=design_file,
            estimated_budget=estimated_budget,
            estimated_duration=estimated_duration
        )
        app.save()
        messages.success(request, "Application applied submitted successfully.")
        return redirect('contractorviewprojects')
    return render(request, 'applyproject.html', context)


def contractorapplications(request):
    if 'contractorid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserLogin.objects.filter(email=contractorid).first()
    application = ContractorApplication.objects.filter(contractor=contractor)
    context = {
        'name': contractor.name,
        'email': contractor.email,
        'profile': contractor.picture,
        'applications': application
    }
    return render(request, 'contractorapplications.html', context)


def assignedprojects(request):
    if 'contractorid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserLogin.objects.filter(email=contractorid).first()
    projects = Project.objects.filter(contractor=contractor)
    context = {
        'contractor': contractor,
        'name': contractor.name,
        'email': contractor.email,
        'profile':contractor.picture,
        'projects': projects,
    }
    return render(request, 'assignedprojects.html', context)

def addprogress(request,id):
    if 'contractorid' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = UserLogin.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'contractor': contractor,
        'name': contractor.name,
        'email': contractor.email,
        'profile':contractor.picture,
        'project': project,
    }
    if request.method == "POST":
        update_text = request.POST.get('update_text')
        image = request.FILES.get('image')
        progress_percent = int(request.POST.get('progress_percent'))
        pu = ProgressUpdate(
            project=project,
            update_text=update_text,
            image=image,
            progress_percent=progress_percent,
            updated_by=contractor
        )
        if progress_percent > 100:
            messages.error(request, "Progress percent cannot be more than 100.")
            return redirect('addprogress', id=id)
        elif progress_percent < 0 or progress_percent < project.progress:
            messages.error(request, "Progress percent cannot be less than current progress.")
            return redirect('addprogress', id=id)
        if progress_percent == 100:
            project.status = 'completed'
        project.progress = progress_percent
        messages.success(request, "Progress update added successfully.")
        pu.save()
        project.save()
        return redirect('assignedprojects')
    return render(request, 'addprogress.html', context)
