from django import template
from index.models import Biodata,Client,Writer,CustomNote,Message,Budget
register = template.Library()

@register.filter(name='skills')
def skills(con):
    try:
        chunks = con.split(',')
        return chunks
    except:
        return None

@register.filter(name='profilepic')
def profilepic(username):
    biodata=Biodata.objects.get(Email=username)
    if biodata.AType=="Writer":
        return Writer.objects.get(Biodata=biodata).Pic.url
    else:
        return Client.objects.get(Biodata=biodata).Pic.url
@register.filter(name="unread")
def unread(username):
    biodata=Biodata.objects.get(Email=username)
    nots=CustomNote.objects.filter(Biodata=biodata, Read=False).count()
    return nots

@register.filter(name="used")
def used(id):
    budget=Budget.objects.get(id=id)
    uamount=budget.Used
    total=budget.Total
    answer=(uamount/total)*100
    return round(answer, 2)

@register.filter(name="remaining")
def remaining(id):
    budget=Budget.objects.get(id=id)
    uamount=budget.Balance
    total=budget.Total
    answer=(uamount/total)*100
    return round(answer, 2)

@register.filter(name="notifications")
def notifications(username):
    biodata=Biodata.objects.get(Email=username)
    nots=CustomNote.objects.filter(Biodata=biodata).order_by("-id")
    for x in nots:
        x.Read=True
        x.save()
    return nots

@register.filter(name="hired")
def hired(props):
    return props.filter(Status="Hired").count()

@register.filter(name="nav")
def nav(username):
    return Biodata.objects.filter(Email=username, AType="Writer").exists()

@register.filter(name="unreadm")
def unreadm(chat):
    unread=Message.objects.filter(Chat=chat, Read=False).filter(Type="Received").count()
    if unread > 0:
        return unread
    else:
        return ""
@register.filter(name="rate")
def rate(no):
    numbers=[]
    try:
        for x in range(0, no):
            numbers.append(x)
        return numbers
    except:
        return [1]



    