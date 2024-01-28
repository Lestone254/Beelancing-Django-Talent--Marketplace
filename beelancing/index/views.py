from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.models import User
from .models import *
from pytz import timezone
import time
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.contrib.auth.decorators import user_passes_test, login_required
# Create your views here.
def index(request):
    templatename="index/index.html"
    return render(request, templatename)

def signin(request):
    if request.user.is_authenticated:
        return redirect("account")
    templatename = "index/login.html"
    context= {}
    if request.method=="POST":
        username=request.POST['semail']
        password=request.POST['spsw']
        next = request.GET.get("next")
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not next == None:
                    print(next)
                    return redirect(next)
                return redirect("account")
            else:
                error ="The password you entered is incorrect !"
                context = {"error":error}
        else:
            error ="No user with the username exists!"
            context={"error":error}
    return render(request, templatename, context)
def signup(request):
    templatename = "index/signup.html"
    if request.method =="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        atype= request.POST['atype']
        email=request.POST['semail']
        password=request.POST['spsw']
        if Biodata.objects.filter(Email=email).exists():
            error = "A User with the same email already exists !"
            context={"error":error}
            return render(request, templatename, context)
        else:
            user=User.objects.create_user(username=email, password=password, email=email, first_name=fname, last_name=lname)
            login(request, user)
            biodata=Biodata()
            biodata.AType=atype
            biodata.Email=email
            biodata.FirstName=fname
            biodata.LastName=lname
            biodata.save()
            wallet=Wallet()
            wallet.User=biodata
            wallet.Balance=0
            wallet.Escrow=0
            wallet.save()
            if biodata.AType=="Writer":
                writer = Writer()
                writer.Biodata=biodata
                writer.Description="None"
                writer.Rate=1
                writer.save()
            else:
                client=Client()
                client.Biodata=biodata
                client.Description="None"
                client.save()
            return redirect('account')
    return render(request, templatename)
@login_required(login_url='/signin')
def out(request):
    logout(request)
    return redirect("signin")

@login_required(login_url='/signin')
def job(request, id):
    templatename="writer/jobpost.html"
    job=Job.objects.get(id=id)
    context= {'job':job}
    return render(request, templatename, context)

def faq(request):
    templatename="index/faq.html"
    return render(request, templatename)

def help(request):
    templatename="index/help.html"
    return render(request, templatename)

def messages(request):
    chats=Chat.objects.filter(From=request.user.username)
    context={"chats":chats}
    templatename="index/messages.html"
    return render(request, templatename, context)

def chat(request, id):
    chat=Chat.objects.get(id=id)
    templatename="index/messagepage.html"
    context={"chat":chat}
    return render(request, templatename, context)

def sendmessage(request):
    message=request.GET.get("body")
    chat=request.GET.get("chat")
    chat=Chat.objects.get(id=chat)
    message1=Message()
    message1.Chat=chat
    message1.Body=message
    message1.Type="Sent"
    message1.save()
    mfrom=chat.To.Email
    biodata=Biodata.objects.get(Email=chat.From)
    chat2=Chat.objects.get(From=mfrom, To=biodata)
    message2=Message()
    message2.Chat=chat2
    message2.Type="Received"
    message2.Body=message
    message2.save()
    templatename="index/messageswindow.html"
    context={'chat':chat}
    return render(request, templatename, context)

def refreshchat(request):
    chat=request.GET.get("chat")
    chat=Chat.objects.get(id=chat)
    context={"chat":chat}
    for x in chat.message_set.all().filter(Read=False):
        x.Read=True
        x.save()
    templatename="index/messageswindow.html"
    return render(request, templatename, context)

def terms(request):
    templatename="index/terms.html"
    return render(request, templatename)

@csrf_exempt
def paypal_webhook(sender, **kwargs):
    ipn_obj = sender
    data = json.loads(sender.body)
    print(data)
    invoice=data["id"]
    print(invoice)
    return JsonResponse({"status":"success"})

valid_ipn_received.connect(paypal_webhook)

def searchpage(request):
    search=request.POST.get("search")
    job1=Job.objects.filter(Title__icontains=search)
    job2=Job.objects.filter(Skills__icontains=search)
    jobs= job1|job2
    context={'jobs':jobs}
    print(jobs)
    templatename="index/searchpage.html"
    return render(request, templatename, context)

@login_required(login_url='/signin')
def nots(request):
    biodata=Biodata.objects.get(Email=username)
    nots=CustomNote.objects.filter(Biodata=biodata)
    templatename="index/notifications"
    return render(request, nots)
