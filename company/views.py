from django.contrib import messages
from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from home.models import Company
import pandas as pd
from django.contrib.auth.models import User
import random
from string import *
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.http import JsonResponse
from home.views import *
# Create your views here.

def temp(request):
    return render(request,"company/temp.html")

def pass_gen(length=8):
    s = ''
    for i in range(length):
        s += random.choice(digits)
    s=str(s)
    return s

def SENDMAIL(subject, message, email):
    try:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )
    except:
        print("Unable to send the email")

def cdashboard(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')

    if request.user.is_authenticated:
        return render(request,"company/cdashboard.html")
    else:
        return redirect('signin')

def change_pass(request):
    email=request.user.email
    myuser=request.user
    # print(email,myuser)
    if send_forgot_email(myuser,email):
        messages.error(request, 'Success - You can change Your password through email sent to you email')
        return redirect('view_profile')
    else:
        messages.error(request, 'Error - Server Error')
        return redirect('view_profile')

def send_forgot_email(user,email):
    myuser=User.objects.get(username=user.username)
    try:
        mycompany=Company.objects.get(user=myuser)
    except:
        try:
            mycompany=Employee.objects.get(user=myuser)
        except:
            print('no User')
            
    if myuser.is_active:
        try:
            myotp=myuser.username + generate_code(60)
            mycompany.otp_code=myotp
            mycompany.save()
            url=settings.BASE_URL_EMAIL+'/Profile/verify/'+myotp
            # print(email)
            email_subject='Password Changing Request In BookDesk'
            email_message='Click this link  to Change Your Password.\n'+'Link:- '+ url
            SENDMAIL(email_subject,email_message,email)
            return True
        except:
            return False

def activate_forgot_by_email(request,code):
    try:
        try:
            profile=Company.objects.get(otp_code=code)
        except:
            profile=Employee.objects.get(otp_code=code)
        if profile.user.is_active:
            myuser=profile.user
            return render(request,'company/changeemail.html',context={})
    except:
        messages.error(request, 'Error - User Not Found Signin to get link again')
        return redirect('home')   

def view_profile(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        temp_email=request.POST.get('email')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        
        verify_email=False   #check to send email
        email=temp_email.lower()
        if email == request.user.email:
            pass
        else:
            verify_email=True    
            
        try:
            myuser=User.objects.get(username=request.user.username)    
            try:
                profile=Company.objects.get(user=myuser)
            except:
                profile=Employee.objects.get(user=myuser)
            myuser.username=username
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            if verify_email:
                myuser.is_active=False
                myuser.email=email
                myuser.save()
                logout(request)
                if send_activate_email(myuser,email):
                    messages.error(request, 'Success - Verification link has been sent to your email verify that.')
                    return redirect('home')
            else:
                messages.error(request, 'Success - Profile Update SuccessFully.')
                return redirect('view_profile')
            
        except:
            messages.error(request, 'Error - Internal Error.')
            return redirect('view_profile')
            
    try:
        profile=Company.objects.get(user=request.user)
    except:
        profile=Employee.objects.get(user=request.user)
    return render(request,'company/profile.html',context={"data":profile})
    
def edashboard(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:        
        
        alldesk=Desk.objects.filter(status=1)
        e_time= '18:00:00'
        for i in alldesk:
                
            now = datetime.now()
            today= now.date()
            today_time=now.time()
            e_date = i.end_date.date()
            end_time=datetime.strptime(e_time,'%H:%M:%S').time()
            if e_date == today:
                if today_time > end_time:
                    # print('hi')
                    i.employee=None
                    i.status=2   
                    i.save()        
            if e_date < today:
                # print('hi')
                i.employee=None
                i.status=2   
                i.save()        
    
        eemployee=Employee.objects.get(user=request.user)
        bookings=Desk.objects.filter(employee=eemployee)
        return render(request,"company/edashboard.html",context={"data":bookings})
    else:
        return redirect('signin')


def mEmployee(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:
        ccompany=Company.objects.get(user=request.user)
        employees = Employee.objects.filter(company=ccompany)
        return render(request,"company/mEmployee.html",context={"data": employees})
        
    else:
        return redirect('signin')

def addEmployee(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.method== "POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('cpassword')

        try:
            User.objects.get(email=email)
            messages.error(request, 'Error - Email Already exists.')
            return redirect('addEmployee')
        except:
            pass

        try:
            User.objects.get(username=username)

            messages.error(request, 'Error - Username Already exists.')
            return redirect('addEmployee')            
        except:
            pass
        
        if not pass1==pass2:
            messages.error(request, 'Error - Entered Passwords are Not same.')
            return redirect('addEmployee')

        email.lower()
        myuser=User.objects.create_user(first_name=fname,last_name=lname,
                                        username=username,email=email)
        
        myuser.set_password(pass1)
        # print(pass1)
        myuser.save()
        
        try:
            company=Company.objects.get(user=request.user)
            Employee.objects.create(user=myuser,company=company)
            
        except Exception as e:
            User.objects.get(id=myuser.id).delete()
            return HttpResponse(str(e))
        email_message='Registeration for Company'
        email_subject='Your Account at BookDesk has been created successfully.'+'\nEmail : '+ email + '\nTemporary Password : ' + str(pass1)
        SENDMAIL(email_message,email_subject,email)
        
        messages.error(request, 'Success - Employee Added Successfully.')
        return redirect('mEmployee')
    company=Company.objects.get(user=request.user)
    return render(request,"company/addEmployee.html", context={"data": company})


def delEmployee(request, id):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:   

        if True:
            employee = Employee.objects.get(id = int(id))

            email=employee.user.email
            employee.user.delete()
            email_message='Account Deletion'
            email_subject='Your Account on BookDesk has been Deleted successfully.'
            SENDMAIL(email_message,email_subject,email)
            # return HttpResponse("User Deleted")
            messages.success(request, 'User Has been deleted.')
            return redirect('mEmployee')

        else:
            # return HttpResponse("database Error ")
            messages.error(request, 'Error - User not found')
            return redirect('mEmployee')
    else:
        return redirect('signin')

def mdesk(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:
        ccompany=Company.objects.get(user=request.user)
        desk = Desk.objects.filter(company=ccompany)
        # desk = Desk.objects.all()
        return render(request,"company/mdesk.html",context={"data": desk})
        
    else:
        return redirect('signin')    

def addDesk(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:
        if request.method=="POST":
            zone=request.POST.get('zone')
            dcount=request.POST.get('deskcount')
            status=request.POST.get('status')
            unique_id=request.POST.get('unique_id')
            
            now = datetime.now()
            today= now.date()
            time=now.time()
            today_datetime = datetime.combine(today , time)
            
            # dcount=int(deskcount)
            dcount=1
            # if dcount > 3 and dcount < 0:
            #     messages.error(request, 'Error - As Said Enter deskcount between 1 and 3')
            #     return redirect('addDesk')
            
            mycompany=Company.objects.get(user=request.user)
            try:
                tempdesk=Desk.objects.create(company=mycompany,zone=zone,monitorCount=dcount,status=status,uniqueID=unique_id,start_date=today_datetime,end_date=today_datetime)
                
                messages.success(request, 'Success - Desk was Added')
                return redirect('mdesk')
            except:
                tempdesk.delete()
                messages.error(request, 'Error - Internal Error')
                return redirect('addDesk')
            
                
            
        else:    
            cdata=request.user.username
            return render(request,"company/addDesk.html",context={"cdata": cdata})
        
    else:    
        return redirect("signin")
    
def desk_upload(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:
        if request.method=="POST":
            file=request.FILES.get('file')
            alldesk=Desk.objects.filter()
            if True:
                if str(file).endswith('.csv'):
                    rfile=pd.read_csv(file)
                elif str(file).endswith('.xlsx'):
                    rfile=pd.read_excel(file)
                else:
                    messages.error(request, 'Error - File Format not valid')
                    return redirect('mdesk')
                
                return desk_uploader(request,rfile,alldesk)
                
            else:
                messages.error(request, 'Error - File not valid')
                return redirect('mdesk')
        
    else:    
        return redirect("signin")
    
def desk_uploader(request,rfile,alldesk):
    mycompany=Company.objects.get(user=request.user)
    if 'MonitorCount' not in rfile.columns:
        messages.error(request, 'Error - No. of desk are imp to provide')
        return redirect('mdesk')
    if 'Status' not in rfile.columns:
        messages.error(request, 'Error - Status of desk is imp to provide')
        return redirect('mdesk')
    if 'Zone' not in rfile.columns:
        messages.error(request, 'Error - Zone of desk is imp to provide')
        return redirect('mdesk')
    if 'UniqueID' not in rfile.columns:
        messages.error(request, 'Error - UniqueID of desk is imp to provide')
        return redirect('mdesk')
    existing_employees=[]
    existing_employees_flag=False
    operation_field= rfile['Zone']
    
    now = datetime.now()
    today= now.date()
    time=now.time()
    today_datetime = datetime.combine(today , time)
    
    for i in range(len(operation_field)):
        
        field=operation_field[i]
        zone=rfile["Zone"][i]
        status=rfile["Status"][i]
        monitorCount=rfile["MonitorCount"][i]
        unique_id=rfile["UniqueID"][i]
        
        try:
            idd=int(unique_id)
            Desk.objects.get(uniqueID=idd)
            existing_employees.append(idd)
            existing_employees_flag=True
            continue
        except:
            pass
        
        desk=Desk.objects.create(company=mycompany,zone=zone,status=status,monitorCount=monitorCount,uniqueID=idd,start_date=today_datetime,end_date=today_datetime)
        
    if existing_employees_flag:
        messages.error(request, 'These Employees exists in your Company:-'+str(existing_employees))
        return redirect('mdesk')    
    else:
        messages.error(request, 'Success - Desks Added Successfully')
        return redirect('mdesk')


def employee_upload(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:
        if request.method=="POST":
            if True:
                file=request.FILES.get('file')
                # allemployees=Desk.objects.filter()
                if True:
                    if str(file).endswith('.csv'):
                        rfile=pd.read_csv(file)
                    elif str(file).endswith('.xlsx'):
                        rfile=pd.read_excel(file)
                    else:
                        messages.error(request, 'Error - File Format not valid')
                        return redirect('mEmployee')
                    
                    return employee_uploader(request,rfile)
                    
                else:
                    messages.error(request, 'Error - File not valid')
                    return redirect('mEmployee')
            else:
                messages.error(request, 'Error - cant read the file')
                return redirect('mEmployee')
        
    else:    
        return redirect("signin")
    
def employee_uploader(request,rfile):
    mycompany=Company.objects.get(user=request.user)

    if 'Email' not in rfile.columns:
        messages.error(request, 'Please add an "Email" column in your file and try uploading again!!')
        return redirect('mEmployee')
    
    invalid_email=[]
    Error_while_generating_employee=[]
    Error_while_generating_employee_flag=False
    invalid_email_flag=False
    
    for i in range(len(rfile['Email'])):
        
        email = rfile["Email"][i]
        fname = rfile["FirstName"][i]
        lname = rfile["LastName"][i]
        employee_id = rfile["EmployeeID"][i]
        
        try:
            User.objects.get(email=email)
            invalid_email.append(email)
            invalid_email_flag=True
            continue
        except:
            pass
        
        email.lower()
        newuser=User.objects.create_user(first_name=fname,last_name=lname,
                                        email=email, username=employee_id)
        pass1 = pass_gen(8)
        newuser.set_password(pass1)
        newuser.save()
        
        try:
            Employee.objects.create(user=newuser,company=mycompany)
        except Exception as e:
            User.objects.get(id=newuser.id).delete()
            Error_while_generating_employee.append(i+1)
            Error_while_generating_employee_flag=True
        
        try:
            email_message='Registeration for Company'
            email_subject='Your Account at BookDesk has been created successfully.'+'Email : '+ email + 'Temporary Password : ' + pass1
            SENDMAIL(email_message,email_subject,email)
        except:
            continue
    if invalid_email_flag ==True and Error_while_generating_employee_flag==True:
        messages.error(request,'Accounts Already exisits for these emails:-'+str(invalid_email)+'System was not able to create account for these employees :-'+str(Error_while_generating_employee))
        return redirect('mEmployee')
    elif invalid_email_flag==True:
        messages.error(request, 'Accounts Already exisits for these emails:-'+str(invalid_email))
        return redirect('mEmployee')
    elif Error_while_generating_employee_flag==True:
        messages.error(request,'System was not able to create account for these employees :-'+str(Error_while_generating_employee))
        return redirect('mEmployee')
    else:
        messages.error(request, 'Success - Employees Added Successfully')
        return redirect('mEmployee')
        
def editDesk(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:
        # print(request.GET)
        main_zone=request.GET.get('zone')
        main_status= request.GET.get('statuss')
        main_monitorCount = request.GET.get('monitorCount')
        main_deskid = request.GET.get('desk_id')
        
        # print(main_deskid,main_status,main_zone,main_monitorCount)
        
        try:
            this_desk= Desk.objects.get(id=main_deskid)
            # print(this_desk)
            
        except:
            messages.error(request, 'Success - Desk Not Found')
            return redirect('mdesk')
        
        try:
            this_desk.zone=main_zone
            this_desk.status=main_status
            this_desk.monitorCount=main_monitorCount
            this_desk.save()
            messages.error(request, 'Success - Desk Updated Successfully')
            return JsonResponse({"error": "Desk Updated"}, status=200)
        except:
            messages.error(request, 'Success - Error While Updating Desk')
            return JsonResponse({"error": "Error While Updating Desk"}, status=400)
            
        
    else:    
        return redirect("signin")

"""
1. next day assign desk from 9 a.m. <-
2. cannot book desk for same day after 6
3. if entered date is next day than desk can be booked for 2 day means for next day and day after tom
4. for day after tom desk can be booked for 1 day
"""
def bookDesk(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:
        if request.method=="POST":
            now = datetime.now()
            today= now.date()
            time=now.time()
            tomorrow = today + timedelta(days = 1)
            day_after_tommorow = today + timedelta(days = 2)
            e_time = '18:00'
            s_time = '09:00'
            
            
            unique_id=request.POST.get('Unique_id')
            date= request.POST.get('date')
            date_till= request.POST.get('date_till')
            # day_main=request.POST.get('desk_days')
            
            # dayss=int(day_main)
            start_desk_time=datetime.strptime(s_time,'%H:%M').time()
            end_time_desk=datetime.strptime(e_time,'%H:%M').time()
            
            booking_date=datetime.strptime(date,'%Y-%m-%d').date()
            end_booking_date=datetime.strptime(date_till,'%Y-%m-%d').date()
            # 1. next day assign desk from 9 a.m.
            if booking_date == today:
                booking_time=time
            else:                
                booking_time=start_desk_time
            
            booking_datetime = datetime.combine(booking_date , booking_time)
            booking_end_datetime = datetime.combine(end_booking_date , end_time_desk)
            
            try:
                temp_employeee=Employee.objects.get(user=request.user)
                temp_deskk=Desk.objects.get(employee= temp_employeee)
                
                if temp_deskk.start_date.date() == booking_date:
                    messages.error(request, 'Error - As per our records you are having Booking for entered details')
                    return redirect('bookDesk') 
                if temp_deskk.end_date.date() == booking_date:
                    messages.error(request, 'Error - You are having Booking of desk for today')
                    return redirect('bookDesk')
                 
                
                # temp_date_desk=booking_date + timedelta(days=1)
                
                # if temp_deskk.end_date.date() == temp_date_desk:
                #     messages.error(request, 'Error - You are having Booking of desk for tommorow')
                #     return redirect('bookDesk') 
                
                # temp_date_desk2=booking_date + timedelta(days=2)
                
                # if temp_deskk.end_date.date() == temp_date_desk2:
                #     messages.error(request, 'Error - You are having Booking of desk for day after tommorow')
                #     return redirect('bookDesk')                 
                
            except:
                pass
            
            if booking_date == today or booking_date == tomorrow or booking_date == day_after_tommorow:
                # 2. cannot book desk for same day after 6
                if booking_time > datetime.strptime('18:00', '%H:%M').time() and end_booking_date==today and booking_date==today:
                    #check existing booking 
               
                    messages.error(request, 'Error - You can not book After 6pm')
                    return redirect('bookDesk')      
                else:
                    try:
                        mydesk=Desk.objects.get(uniqueID=unique_id)
                        pass
                    except:
                        messages.error(request, 'Error - Desk id not valid')
                        return redirect('bookDesk') 
                    thisdesk=int(mydesk.status)
                    # print(thisdesk)
                    
                    if thisdesk==2:
                        mydesk.start_date=booking_datetime
                        end_date_desk=end_booking_date
                        
                        mydesk.end_date=datetime.combine(end_date_desk,end_time_desk)
                        
                        mydesk.employee=temp_employeee         
                        mydesk.status= 1
                        mydesk.save()
                        messages.error(request, 'Success - This Desk is Booked for you')
                        return redirect('bookDesk') 
                        
                    else:
                        messages.error(request, 'Error - This Desk is not available')
                        return redirect('bookDesk')     
            else:
                messages.error(request, 'Error - You can not book for more than 2 days')
                return redirect('bookDesk')
                
        else:        
            alldesk=Desk.objects.filter(status=1)
            e_time= '18:00:00'
            for i in alldesk:
                
                now = datetime.now()
                today= now.date()
                today_time=now.time()
                # print(today_time)
                e_date = i.end_date.date()
                end_time=datetime.strptime(e_time,'%H:%M:%S').time()
                if e_date == today:
                    if today_time > end_time:
                        # print('hi')
                        i.employee=None
                        i.status=2   
                        i.save()          
            
            companyy=Employee.objects.get(user = request.user).company
            avail_temp=2
            availDesk=Desk.objects.filter(company=companyy,status=avail_temp)
            return render(request,"company/bookDesk.html",context={'data':availDesk})
    else:    
        return redirect("signin")