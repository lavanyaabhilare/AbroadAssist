from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import math
from django.db import IntegrityError
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
import random
from .models import user_otp
from django.core.mail import send_mail
from django.conf import settings

   

def send_email(receiver_email,OTP,rs="abc"):
    if rs == "forgot":
        subject = "Your password"
        message = f""" Your Password is {OTP} for verification on abroad assits"""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [receiver_email]
        send_mail(subject, message, email_from, recipient_list)

    else:  
        print(OTP)

        subject = "OTP for Verification"
        message = f""" Your otp is {OTP} for verification on abroad assits"""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [receiver_email]
        send_mail(subject, message, email_from, recipient_list)
        return OTP

    

# Example usage:
def otpvery(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        otp = request.POST['otp']
       
        obj = user_otp.objects.filter(email=email).values("gen_otp")
       
        for i in obj:
          
            if i['gen_otp'] == int(otp):
                print("auth")
                try:
                    us = User.objects.create_user(username=username,email=email,password=password)
                    us.save()
                except IntegrityError as e:
                    context = {"msg":"Username already exist try using forgot password"}
                    return render(request,"login.html",context)
                
                us = authenticate(request , username=username , password=password)
                print(us)
                if us is not None:
                    print("saved")
                    login(request,us)
                    return redirect("/")
            
    else:
        return redirect("login")



def log(request):
    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password'] 
        print(user,password) 
        obj = authenticate(username=user,password=password)
        print(obj,"\n")
        if obj is not None:
            login(request,obj)
            return redirect("/")

    return render(request, "login.html")

@login_required
def dashboard(request):

    return redirect("/pages/dashboard")

@login_required
def logot(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        digits = "0123456789"
        otp = ""
        for i in range(6) :
            otp += digits[math.floor(random.random() * 10)]
        try:
            inst = user_otp(username=username, email=email, password=password, gen_otp=otp)
            inst.save()
            send_email(email, otp)
        except IntegrityError as e:
            print(f"Integrity Error: {e}")
            obj = user_otp.objects.filter(email=email).first()
            otp = obj.gen_otp
            send_email(email, otp)
        except Exception as e:
            print(f"Error during save: {e}")

        context = {"username":username,"email":email,"password":password}
        return render(request,"otp.html",context)
    
    else:
        return render(request,"signup.html")

def forpass(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            pas = user_otp.objects.get(email=email)  # Get the user_otp object for the given email
            obj= pas.password 
            print(obj)
            send_email(email,obj,"forgot") 
            return render(request,"login.html",{"msg":"Password is send to Mail"})
        except:
            context = {"msg":"Gmail witth this id doesn't exist"}
            return render(request,"forget_pass.html",context)
    
    return render(request,"forget_pass.html",{"msg":""})

def router(request,page):
    page = page+".html"
    return render(request,page)
