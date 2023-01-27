from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from staff.models import Plan
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from company.models import Employee
import math
import random
# Create your views here.
def SENDMAIL(subject, message, email):
    try:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )
    except:
        print("Unable to send the email")
        
def generate_code(length):
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(length) :
        code += digits[math.floor(random.random() * 62)]
    return code

def home(request):
    plans = Plan.objects.all().order_by('price').values
    return render(request,"home/home.html", context={"data": plans})

def signout(request):
    logout(request)
    return redirect('home')

def forgot_pass(request):
    if request.method=='POST':
        temp_email=request.POST.get('email')
        
        email=temp_email.lower()
        myuser=User.objects.get(email=email)
        if send_forgot_email(myuser,email):
            messages.error(request, 'Success - Your Request for Forgot Password has been approved, You can Check your Email.')
            return redirect('home')
        else:
            messages.error(request, 'Error - Server Error')
            return redirect('home')
        
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
        
# Staff
def signin(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        temp_uemail=request.POST.get('ename')
        password=request.POST.get('password')
        
        uemail=temp_uemail.lower()
            
        # resend code
        try:
            verify_user=User.objects.get(username=uemail)    
        except:
            verify_user=User.objects.get(email=uemail)    
        # print(verify_user.email)
        if verify_user.is_active == False:
            # print('hi')
            if send_activate_email(verify_user,verify_user.email):
                messages.error(request, 'Success - Your Email is not yet verified. So we have Sent Link to your email verify that to continue')
                return redirect('home')  
        try:
            tempuser=User.objects.get(email=uemail).username                  
            user=authenticate(request,username=tempuser,password=password)
            # print(user)
        except:
            try:
                User.objects.get(username=uemail)
                
                user=authenticate(request,username=uemail,password=password)
                
            except:    
                messages.error(request, 'Error - Entered Username or Email is Not in our records.')
                return redirect('signin')
        
        # print(user)            
        if user == None: 
            messages.error(request, 'Error - No User Exists.')
            return redirect('signin')
        
        if user.is_active:
            login(request,user)
            return redirect('dashboard')
        
        else:
            messages.error(request, 'Error - You dont have permission to login.')
            return redirect('signin')
            # return HttpResponse( 'You dont have staff permission')
        
    else:
        return render(request,"home/signin.html")

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    if request.user.is_superuser:
        signout(request)
        messages.error(request, 'Error - Super user cannot signin Here.')
        return redirect('home')

    if request.user.is_staff:
        return redirect('staffdashboard')    

    try:
        Company.objects.get(user = request.user)
        return redirect('cdashboard')
    except:
        try:
            Employee.objects.get(user=request.user)
            return redirect('edashboard')
        except:
            messages.error(request, 'Error - You Dont have Access to our Dashboard.')
            return redirect('signin')
def send_activate_email(user,email):
    myuser=User.objects.get(username=user.username)
    try:
        mycompany=Company.objects.get(user=myuser)
    except:
        try:
            mycompany=Employee.objects.get(user=myuser)
        except:
            print('No User Found')
    if not myuser.is_active:
        try:
            myotp=myuser.username + generate_code(60)
            mycompany.otp_code=myotp
            mycompany.save()
            url=settings.BASE_URL_EMAIL+'/signup/verify/'+myotp
            # print(email)
            email_subject='Account Verification Request In BookDesk'
            email_message='You need To veriy you email in order to continue to our website\n'+'Activation Link:- '+ url
            SENDMAIL(email_subject,email_message,email)
            return True
        except:
            return False

def activate_by_email(request,code):
    try:
        try:
            profile=Company.objects.get(otp_code=code)
        except:
            try:
                profile=Employee.objects.get(otp_code=code)
            except:
                print('User Not Found')
        if profile.user.is_active:
            return render(request,'home/email.html')
        myuser=profile.user
        myuser.is_active=True
        myuser.save()
        email=myuser.email
        try:
            email_message='Account Verified In BookDesk'
            email_subject='Your Account at BookDesk has been created Verified Visit our page to avail amazing experience'
            SENDMAIL(email_message,email_subject,email)
        except Exception as e:
            print("Can't send email\n", str(e))

        return render(request,'home/email.html')
    except:
        messages.error(request, 'Error - User Not Found Signin to get link again')
        return redirect('home')    
    

def activate_forgot_by_email(request,code):
    try:
        profile=Company.objects.get(otp_code=code)
        
    except:
        try:
            profile=Employee.objects.get(otp_code=code)
        except:
            messages.error(request, 'Error - User Not Found Signin to get link again')
            return redirect('home')
    myuser=profile.user
    return render(request,'home/changeemail.html',context={"data":myuser})

def signup(request, plan_id):
    if request.method== "POST":
        temp_username=request.POST.get('username')
        temp_email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('cpassword2')
        plan_id=request.POST.get('plan_id')
        location=request.POST.get('location')

        email=temp_email.lower()
        username=temp_username.lower()
        
        if not pass1==pass2:
            messages.error(request, 'Error - Entered Passwords are same.')
            return redirect('signup', plan_id)
        
        try:
            plan=Plan.objects.get(id=int(plan_id))
        except:
            messages.error(request, 'Error - Select a valid plan.')
            return redirect('signup', plan_id)


        try:
            User.objects.get(email=email)
            messages.error(request, 'Error - Email Already exists.')
            return redirect('signup', plan_id)
        except:
            pass

        try:
            User.objects.get(username=username)

            messages.error(request, 'Error - Username Already exists.')
            return redirect('signup', plan_id)            
        except:
            pass
        

        # email.lower()
        # username.lower()
        myuser=User.objects.create_user(username=username,email=email)
        myuser.is_active=False
        myuser.set_password(pass1)
        myuser.save()

        try:
            Company.objects.create(user=myuser, 
                                plan=plan,
                                location=location)
        except Exception as e:
            User.objects.get(id=myuser.id).delete()
            return HttpResponse(str(e))
        
        if send_activate_email(myuser,email):
            messages.error(request, 'Success - Verification link has been sent to your email. So Check You email and verify You email within 3 min otherwise link will expire')
            return redirect('home')
        else:
            messages.error(request, 'Error - Unable to send Notification. But your Account has been created but you will not be able to login as it is inactive so signin to resend link')
            return redirect('home')

    try:
        plan = Plan.objects.get(id = int(plan_id))
    except:
        messages.error(request, 'Error - No plan selected.')
        return redirect('home')

    return render(request,"home/signup.html", context={"plan": plan})

def email_for_change_verified(request):
    
    if request.method == 'POST':
        request.POST
        temp_email=request.POST.get('email')
        pass1=request.POST.get('password')
        cpass=request.POST.get('cpassword')
        
        email=temp_email.lower()
        # print(email,temp_email)
        try:
            myuser=User.objects.get(email=email)
            if not pass1==cpass:
                messages.error(request, 'Error - Entered Passwords are same.')
                return redirect('email_for_change_verified')
            myuser.set_password(pass1)
            myuser.save()
            logout(request)
            messages.error(request, 'Success - Password Changed Successfully')
            return redirect('home')
            
        except:
            messages.error(request, 'Error - User Not Found.')
            return redirect('home')
        
    return render(request,"company/changepass.html", context={})