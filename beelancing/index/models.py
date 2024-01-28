from email.policy import default
from django.db import models
from pytz import timezone
from datetime import datetime


class Biodata(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=60)
    Email = models.CharField(max_length=100)
    AType = models.CharField(max_length=50)

    class Meta:
        ordering = ['-id']

    def full_name(self):
        return f'{self.FirstName} {self.LastName}'


class Client(models.Model):
    Biodata = models.ForeignKey(Biodata, on_delete=models.CASCADE)
    Pic = models.ImageField(max_length=1000, upload_to='profiles', default='profiles/avatar.png')

    class Meta:
        ordering = ['-id']


class Writer(models.Model):
    Biodata = models.ForeignKey(Biodata, on_delete=models.CASCADE)
    Pic = models.ImageField(max_length=1000, upload_to='profiles', default='profiles/avatar.png')
    Description = models.TextField(default="None")
    Skills = models.TextField(null=True)
    Profesion = models.TextField(null=True)
    Rate = models.IntegerField(null=True)
    CV = models.FileField(upload_to="cvs", null=True, default="cv.default")
    Availability = models.IntegerField(null=True)

    class Meta:
        ordering = ['-id']


class Job(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Category = models.CharField(max_length=100)
    Skills = models.TextField()
    Type = models.CharField(max_length=100)
    Amount = models.IntegerField()
    Rate = models.CharField(max_length=100)
    DateTime = models.DateTimeField()
    Status = models.CharField(default="Open", max_length=100)
    Level = models.CharField(max_length=100, null=True)
    Client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    Duration = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ['-id']


class SavedJob(models.Model):
    Job = models.ForeignKey(Job, on_delete=models.CASCADE)
    Writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    Time = models.DateTimeField()

    class Meta:
        ordering = ['-id']


class Proposal(models.Model):
    Job = models.ForeignKey(Job, on_delete=models.CASCADE)
    Writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    Status = models.CharField(max_length=100, default="Open")
    Body = models.TextField()
    Sent = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ['-id']


class File(models.Model):
    File = models.FileField(upload_to='proposals')
    Proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class Notification(models.Model):
    Message = models.TextField()
    Time = models.DateTimeField(default=datetime.now())
    Target = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']


class CustomNote(models.Model):
    Notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    Biodata = models.ForeignKey(Biodata, on_delete=models.CASCADE)
    Read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']


class Chat(models.Model):
    From = models.CharField(max_length=100)
    To = models.ForeignKey(Biodata, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class Message(models.Model):
    Chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    Body = models.TextField()
    Type = models.CharField(max_length=100)
    DateTime = models.DateTimeField(default=datetime.now())
    Read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']


class Review(models.Model):
    Rate = models.IntegerField()
    User = models.ForeignKey(Biodata, on_delete=models.CASCADE)
    Review = models.TextField()
    Client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class SavedWriter(models.Model):
    Writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    Client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Time = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ['-id']


class Hire(models.Model):
    Proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    Client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    Budget = models.IntegerField()
    Escrow = models.IntegerField()
    Time = models.DateTimeField(default=datetime.now())


class JobUnpaid(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Category = models.CharField(max_length=100)
    Skills = models.TextField()
    Type = models.CharField(max_length=100)
    Amount = models.IntegerField()
    Rate = models.CharField(max_length=100)
    DateTime = models.DateTimeField()
    Status = models.CharField(default="Open", max_length=100)
    Level = models.CharField(max_length=100, null=True)
    Client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    Duration = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ['-id']


class Budget(models.Model):
    Job = models.ForeignKey(Job, on_delete=models.CASCADE)
    Client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Used = models.IntegerField()
    Total = models.IntegerField()
    Balance = models.IntegerField()

    class Meta:
        ordering = ['-id']


class Transaction(models.Model):
    User = models.ForeignKey(Biodata, on_delete=models.CASCADE)
    Reference = models.CharField(max_length=100)
    Time = models.DateTimeField()
    Type = models.CharField(max_length=100)
    Description = models.TextField()
    Amount = models.IntegerField()
    FreeLancer = models.ForeignKey(Writer, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-id']


class Wallet(models.Model):
    User = models.ForeignKey(Biodata, on_delete=models.CASCADE)
    Escrow = models.IntegerField()
    Balance = models.IntegerField()

    class Meta:
        ordering = ['-id']


class Disputes(models.Model):
    Client = models.ForeignKey(Biodata, on_delete=models.CASCADE)
    Subject = models.CharField(max_length=150)
    Department = models.CharField(max_length=30)
    Priority = models.CharField(max_length=30)
    Message = models.TextField()
    Image = models.ImageField(max_length=1000, upload_to='dispute', null=True)
    Date_filed = models.DateTimeField(auto_now_add=True)
    Closed = models.BooleanField(default=False)
