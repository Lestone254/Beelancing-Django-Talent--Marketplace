from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
# Create your views here.
from re import template
from django.shortcuts import render, redirect
from index.models import *
from django.contrib.auth.decorators import user_passes_test, login_required
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta

def checkw(user):
    return Biodata.objects.filter(Email=user.username, AType="Writer").exists()

@login_required(login_url='/signin')
def account(request):
    username=request.user.username
    if Biodata.objects.filter(AType="Writer", Email=username):
        return redirect("dashboard")
    else:
        return redirect("clientdash")

@user_passes_test(checkw, login_url='/signin/')
def dashboard(request):
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    jobs = Job.objects.all().order_by("-id").exclude(Status="Closed")
    savedjobs=SavedJob.objects.filter(Writer=writer)
    templatename= "writer/dashboard.html"
    one_day_ago = datetime.now() - timedelta(days=1)
    recent=Job.objects.filter(DateTime__range=(one_day_ago, datetime.now())).order_by("-id").exclude(Status="Closed")
    context={'jobs':jobs, 'savedjobs':savedjobs, 'recent':recent}
    return render(request, templatename, context)

@user_passes_test(checkw, login_url='/signin/')
def settings(request):
    templatename = "writer/settings.html"
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    context = {"biodata":biodata, "writer":writer}
    return render(request, templatename, context)

@user_passes_test(checkw, login_url='/signin/')
def profile(request):
    templatename = "writer/profile.html"
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    context = {"biodata":biodata, 'writer':writer}
    return render(request, templatename, context)

@user_passes_test(checkw, login_url='/signin/')
def savejob(request, id):
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    job = Job.objects.get(id=id)
    if not SavedJob.objects.filter(Job=job, Writer=writer).exists():
        savedjob=SavedJob()
        savedjob.Job=job
        savedjob.Writer=writer
        savedjob.Time=datetime.now()
        savedjob.save()
    return redirect('dashboard')

@user_passes_test(checkw, login_url='/signin/')
def editprop(request, id):
    templatename="writer/applyjob.html"
    job=Job.objects.get(id=id)
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    if Proposal.objects.filter(Job=job, Writer=writer).exists():
        return redirect('proposals')
    context={'job':job}
    return render(request, templatename, context)

@user_passes_test(checkw, login_url='/signin/')
def removejob(request, id):
    savedjob= SavedJob.objects.filter(id=id)
    if savedjob.exists():
        savedjob=SavedJob.objects.get(id=id)
        savedjob.delete()
    return redirect('savedjobs')

@user_passes_test(checkw, login_url='/signin/')
def allcontracts(request):
    templatename="writer/allcontracts.html"
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    active=Proposal.objects.filter(Writer=writer, Status="Open")
    archived = Proposal.objects.filter(Writer=writer, Status="Archived")
    context = {'active':active, 'archived':archived}
    return render(request, templatename, context)

@user_passes_test(checkw, login_url='/signin/')
def savedjobs(request):
    templatename="writer/savedjobs.html"
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    savedjobs=SavedJob.objects.filter(Writer=writer)
    context={'savedjobs':savedjobs}
    return render(request, templatename, context)

@user_passes_test(checkw, login_url='/signin/')
def proposals(request):
    templatename= "writer/proposals.html"
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    active=Proposal.objects.filter(Writer=writer, Status="Open")
    archived = Proposal.objects.filter(Writer=writer, Status="Archived")
    context = {'active':active, 'archived':archived}
    return render(request, templatename, context)

@user_passes_test(checkw, login_url='/signin/')
def applyjob(request):
    biodata=Biodata.objects.get(Email=request.user.username)
    writer=Writer.objects.get(Biodata=biodata)
    if request.method=="POST":
        files = request.FILES.getlist('files')
        body=request.POST.get('proposal')
        job=request.POST.get('job')
        job=Job.objects.get(id=job)
        if not Proposal.objects.filter(Job=job, Writer=writer).exists():
            proposal=Proposal()
            proposal.Body=body
            proposal.Writer=writer
            proposal.Job=job
            proposal.save()
            for file in files:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_url = fs.url(filename)
                f=File()
                f.File=filename
                f.Proposal=proposal
                f.save()
    return redirect('dashboard')


@user_passes_test(checkw, login_url='/signin/')
def editpic(request):
    pic=request.FILES.get("pic")
    email=request.user.username
    biodata=Biodata.objects.get(Email=email)
    writer=Writer.objects.get(Biodata=biodata)
    fs = FileSystemStorage()
    filename = fs.save(pic.name, pic)
    file_url = fs.url(filename)
    writer.Pic=filename
    writer.save()
    return redirect("settings")


@user_passes_test(checkw, login_url='/signin/')
def updatebio(request):
    bio=request.POST.get("bio")
    skills=request.POST.get("skills")
    email=request.user.username
    biodata=Biodata.objects.get(Email=email)
    writer=Writer.objects.get(Biodata=biodata)
    writer.Skills=skills
    writer.Description=bio
    writer.save()
    return redirect("settings")

def searchjob(request):
    search=request.GET.get("search")
    job1=Job.objects.filter(Title__icontains=search)
    job2=Job.objects.filter(Skills__icontains=search)
    jobs= job1|job2
    context={'jobs':jobs}
    templatename="writer/searchtalent.html"
    return render(request, templatename, context)

@login_required(login_url='/signin')
def startchat(request, email):
    if Chat.objects.filter(From=request.user.username, To=Biodata.objects.get(Email=email)):
        chat=Chat.objects.get(From=request.user.username, To=Biodata.objects.get(Email=email))
        templatename="index/messagepage.html"
        context={"chat":chat}
    else:
        chat1=Chat()
        chat1.From=request.user.username
        chat1.To=Biodata.objects.get(Email=email)
        chat1.save()
        chat2=Chat()
        chat2.From=email
        chat2.To=Biodata.objects.get(Email=request.user.username)
        chat2.save()
        templatename="index/messagepage.html"
        context={"chat":chat1}
    return render(request, templatename, context)

def change(request):
    if request.method == 'POST':
        new_password1 = request.POST['newpassword']
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return redirect('settings')





