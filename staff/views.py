from pyexpat.errors import messages
from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib import messages
# Create your views here.

def setplan(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_staff:
        plans = Plan.objects.all()
        return render(request,"staff/setplan.html", context={"data" : plans})
        # plans = Plan.objects.all()
        # return render(request,'staff/setplan.html',context={"all_plans": plans})
    messages.error(request, 'Error - You dont have staff permission Signin with staff account.')
    return redirect('home')
    

def addplan(request):
    
    if request.method == 'POST':
        name=request.POST.get('planname')
        description=request.POST.get('plandesc')
        price=request.POST.get('planprice')

        Plan.objects.create(name=name,description=description, price=price)

        messages.error(request, 'Success - Plan Added Successfully.')
        return redirect('setplan')

    # plans = Plan.objects.all()
    else:
        if request.user.is_superuser:
            logout(request)
            messages.error(request, 'Error - Super user Dont have Access.')
            return redirect('home')
        if request.user.is_staff:
            return render(request,"staff/addplan.html")
        else:
            messages.error(request, 'Error - You dont have staff permission Signin with staff account.')
            return redirect('home')

def delplan(request,plan_id):
    try :
        thisplan=Plan.objects.get(id=int(plan_id))
        thisplan.delete()
        messages.error(request, 'Success - Plan Deleted Successfully.')
        return redirect('setplan')

    except:
        messages.error(request, 'Error - Enter Valid plan listed Below.')
        return redirect('setplan')
    
def staffdashboard(request):
    
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    return render(request,"staff/staffdashboard.html")
