from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, reverse
from index.models import *
from datetime import datetime
from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test, login_required


def checkc(user):
    return Biodata.objects.filter(Email=user.username, AType="Client").exists()


@user_passes_test(checkc, login_url='/signin/')
def clientdash(request):
    templatename = "client/dashboard.html"
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    jobs = Job.objects.filter(Client=client).order_by("-id")
    one_day_ago = datetime.now() - timedelta(days=1)
    recent = Job.objects.filter(Client=client, DateTime__range=(one_day_ago, datetime.now())).order_by("-id")
    talent = Writer.objects.all().order_by("-Rate")[:5]
    context = {'jobs': jobs, 'talent': talent, 'recent': recent}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def addjob(request):
    templatename = "client/upload.html"
    return render(request, templatename)


@user_passes_test(checkc, login_url='/signin/')
def postjob(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    title = request.POST.get("title")
    category = request.POST.get("category")
    description = request.POST.get("desc")
    projecttype = request.POST.get("projecttype")
    duration = request.POST.get("duration")
    level = request.POST.get("level")
    rate = request.POST.get("rate")
    amount = int(request.POST.get("amount"))
    skills = request.POST.get("skills")
    job = JobUnpaid()
    job.Client = client
    job.Skills = skills
    job.Description = description
    job.Level = level
    job.Title = title
    job.Category = category
    job.Duration = duration
    job.Amount = amount
    job.Type = projecttype
    job.Rate = rate
    job.DateTime = datetime.now()
    job.save()
    return initiate(request, job.id)


@user_passes_test(checkc, login_url='/signin/')
def myjobs(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    jobs = Job.objects.filter(Client=client).order_by("-id")
    templatename = "client/jobpostings.html"
    one_day_ago = datetime.now() - timedelta(days=1)
    recent = Job.objects.filter(Client=client, DateTime__range=(one_day_ago, datetime.now())).order_by("-id")
    context = {'jobs': jobs, 'recent': recent}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def alljobs(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    jobs = Job.objects.all().exclude(Status="Closed").order_by("-id")
    templatename = "client/allpostings.html"
    context = {'jobs': jobs}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def discovertalent(request):
    writers = Writer.objects.all()
    templatename = "client/discovertalent.html"
    context = {'writers': writers}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def viewprofile(request, id):
    biodata = Biodata.objects.get(id=id)
    writer = Writer.objects.get(Biodata=biodata)
    templatename = "client/viewprofile.html"
    context = {"biodata": biodata, "writer": writer}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def searchtalent(request):
    search = request.GET.get("search")
    bio1 = Biodata.objects.filter(FirstName__icontains=search, AType="Writer")
    bio2 = Biodata.objects.filter(LastName__icontains=search, AType="Writer")
    bios = bio1 | bio2
    print(bios)
    context = {'bios': bios}
    templatename = "client/searchtalent.html"
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def viewproposals(request, id):
    job = Job.objects.get(id=id)
    templatename = "client/proposals.html"
    context = {'job': job}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def proposal(request, id):
    proposal = Proposal.objects.get(id=id)
    templatename = "client/viewproposal.html"
    context = {"proposal": proposal}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def rate(request):
    body = request.POST.get("review")
    user = request.POST.get("writer")
    rate = request.POST.get("rate")
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    review = Review()
    review.Review = body
    review.Client = client
    review.User = Biodata.objects.get(Email=user)
    review.Rate = rate
    review.save()
    writer = Biodata.objects.get(Email=user)
    writer = Writer.objects.get(Biodata=writer)
    biodata = Biodata.objects.get(Email=user)
    templatename = "client/viewprofile.html"
    context = {"biodata": biodata, "writer": writer}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def savewriter(request, id):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    writer = Writer.objects.get(id=id)
    if not SavedWriter.objects.filter(Client=client, Writer=writer).exists():
        savedwriter = SavedWriter()
        savedwriter.Client = client
        savedwriter.Writer = writer
        savedwriter.save()
    return redirect('savedwriters')


@user_passes_test(checkc, login_url='/signin/')
def savedwriters(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    writers = []
    for x in SavedWriter.objects.filter(Client=client):
        writers.append(x.Writer)
    templatename = "client/discovertalent.html"
    context = {'writers': writers}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def initiate(request, unpaid):
    # What you want the button to do.
    job = JobUnpaid.objects.get(id=unpaid)
    paypal_dict = {
        "business": "sb-znda423959015@business.example.com",
        "amount": job.Amount,
        "item_name": job.Title,
        "invoice": "HOY" + str(job.id),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('paymentcomplete')),
        "cancel_return": request.build_absolute_uri(reverse('paymentwrong')),
    }

    # Create the instance.
    request.session['unpaidjob'] = job.id
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "job": job}
    return render(request, "client/complete.html", context)


@user_passes_test(checkc, login_url='/signin/')
def paymentcomplete(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    paidjob = JobUnpaid.objects.filter(Client=client).first()
    job = Job()
    job.Client = paidjob.Client
    job.Skills = paidjob.Skills
    job.Description = paidjob.Description
    job.Level = paidjob.Level
    job.Title = paidjob.Title
    job.Category = paidjob.Category
    job.Duration = paidjob.Duration
    job.Amount = paidjob.Amount
    job.Type = paidjob.Type
    job.Rate = paidjob.Rate
    job.DateTime = datetime.now()
    job.save()
    trans = Transaction()
    trans.User = biodata
    trans.Amount = job.Amount
    trans.Reference = "HOY" + str(paidjob.id)
    trans.Time = datetime.now()
    trans.Type = "Job Listing"
    trans.Description = "Invoice for listing of " + job.Title
    trans.save()
    paidjob.delete()
    budget = Budget()
    budget.Client = client
    budget.Job = job
    budget.Used = 0
    budget.Balance = job.Amount
    budget.Total = job.Amount
    budget.save()
    wallet = Wallet.objects.get(User=biodata)
    wallet.Escrow = wallet.Escrow + job.Amount
    wallet.save()
    context = {"job": job}
    templatename = "client/success.html"
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def paymentwrong(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    job = JobUnpaid.objects.filter(Client=client).first()
    context = {"job": job}
    templatename = "client/failed.html"
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def budget(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    templatename = "client/budget.html"
    budgets = Budget.objects.filter(Client=client)
    context = {"budgets": budgets}
    return render(request, templatename, context)


def history(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    history = Transaction.objects.filter(User=biodata)
    wallet = Wallet.objects.get(User=biodata)
    templatename = "client/history.html"
    context = {"history": history, "wallet": wallet}
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def hire(request, id):
    biodata = Biodata.objects.get(Email=request.user.username)
    proposal = Proposal.objects.get(id=id)
    writer = proposal.Writer
    writer = writer.Biodata
    job = proposal.Job
    job.Status = "Closed"
    job.save()
    proposal.Status = "Hired"
    proposal.save()
    for props in Proposal.objects.filter(Job=job).exclude(id=id):
        props = "Job Closed"
        props.save()
    message = "Hello {fname} !,We come bearing good your! Your proposal for the job labeled: {jobtitle} has been " \
              "accepted. Log into your account for details".format(
        fname=biodata.FirstName, jobtitle=job.Title)
    send_mail('Proposal Accepted', message, 'info@beelancing.com', [writer.Email], fail_silently=False, )
    return redirect("hires")


@user_passes_test(checkc, login_url='/signin/')
def hires(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    jobs = Job.objects.filter(Client=client).order_by("-id")
    proposals = []
    for job in jobs:
        for x in job.proposal_set.all().filter(Status="Hired"):
            proposals.append(x)
    context = {"proposals": proposals}
    templatename = "client/myhires.html"
    return render(request, templatename, context)


@user_passes_test(checkc, login_url='/signin/')
def allcontracts(request):
    biodata = Biodata.objects.get(Email=request.user.username)
    client = Client.objects.get(Biodata=biodata)
    jobs = Job.objects.filter(Client=client).order_by("-id")
    proposals = []
    for job in jobs:
        for x in job.proposal_set.all().filter(Status="Hired"):
            proposals.append(x)
    context = {"proposals": proposals}
    templatename = "client/allcontracts.html"
    return render(request, templatename, context)


def tickets(request):
    client = Biodata.objects.get(Email=request.user.username)
    recent_tickets = Disputes.objects.filter(Client=client)
    templatename = 'client/ticket.html'
    context = {'recent_tickets': recent_tickets}
    return render(request, templatename, context)


def open_tickect(request):
    client = Biodata.objects.get(Email=request.user.username)
    recent_tickets = Disputes.objects.filter(Client=client)
    if request.method == 'POST':
        client = Biodata.objects.get(Email=request.user.username)
        subject = request.POST.get('subject')
        department = request.POST.get('department')
        priority = request.POST.get('priority')
        image = request.FILES['file']
        message = request.POST.get('message')

        new_dispute = Disputes()
        new_dispute.Client = client
        new_dispute.Subject = subject
        new_dispute.Department = department
        new_dispute.Image.save(image.name, image)
        new_dispute.Priority = priority
        new_dispute.Message = message
        new_dispute.save()
        return redirect('tickets')
    templatename = 'client/openticket.html'
    context = {'recent_tickets': recent_tickets}
    return render(request, templatename, context)


def mytickets(request):
    client = Biodata.objects.get(Email=request.user.username)
    details = Biodata.objects.filter(Email=request.user.username)
    for i in details:
        print(i.AType)
    disputes = Disputes.objects.filter(Client=client).order_by('-Date_filed')
    paginator = Paginator(disputes, 3)  # set 2 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    templatename = 'client/mytickets.html'
    context = {'page_obj': page_obj}
    return render(request, templatename, context)
