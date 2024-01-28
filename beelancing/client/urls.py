from django.urls import path
from .views import *

urlpatterns = [
    path("", clientdash, name="clientdash"),
    path("addjob/", addjob, name="addjob"),
    path("postjob", postjob, name="postjob"),
    path("myjobs/", myjobs, name="myjobs"),
    path("discover/", discovertalent, name="discover"),
    path("viewprofile/<int:id>/", viewprofile, name="viewprofile"),
    path("searchtalent/", searchtalent, name="searchtalent"),
    path("proposals/<int:id>", viewproposals, name="viewproposals"),
    path("proposal/<int:id>", proposal, name="proposal"),
    path("rate/", rate, name="rate"),
    path("savetalent/<int:id>", savewriter, name="savewriter"),
    path("savedtalent/", savedwriters, name="savedwriters"),
    path("success/", paymentcomplete, name="paymentcomplete"),
    path("failed/", paymentwrong, name="paymentwrong"),
    path("budget/", budget, name="budgets"),
    path("history/", history, name="history"),
    path("hire/<int:id>/", hire, name="hire"),
    path("allpostings/", alljobs, name="alljobs"),
    path("hire/<int:id>", hire, name="hire"),
    path("hires/", hires, name="hires"),
    path("allcontracts/", allcontracts, name="allcontracts"),
    path("tickets/", tickets, name="tickets"),
    path("openticket/", open_tickect, name="openticket"),
    path("mytickets/", mytickets, name='mytickets')
]

