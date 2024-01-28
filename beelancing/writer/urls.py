from django.urls import path
from .views import *

urlpatterns = [
    path("", account, name="account"),
    path("dashboard/", dashboard, name="dashboard"),
    path("profile/", profile, name="profile"),
    path("settings/", settings, name="settings"),
    path("proposals/", proposals, name="proposals"),
    path("savejob/<int:id>/", savejob, name="savejob"),
    path("editprop/<int:id>/", editprop, name="editprop"),
    path("removejob/<int:id>/", removejob, name="removejob"),
    path("applyjob/", applyjob, name="applyjob"),
    path("savedjobs/", savedjobs, name="savedjobs"),
    path("allcontracts/", allcontracts, name="allcontracts"), 
    path("editpic/", editpic, name="editpic"), 
    path("updatebio/", updatebio, name="updatebio"),  
    path("searchjob/", searchjob, name="searchjob"), 
    path("change/", change, name="change"),
    path("startchat/<str:email>/", startchat, name="startchat"), 
]
