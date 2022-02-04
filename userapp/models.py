from distutils.command.upload import upload
from email.policy import default
from tkinter import CASCADE
from xml.parsers.expat import model
from django.db import models

# Create your models here.
class UserDetNew(models.Model):
    c= (
        ('Doc','Doctor'),
        ('Patients','Patients')
    )
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    username =  models.CharField(max_length=20,unique=True)
    profile_pic = models.ImageField(upload_to="uploads/pimg/")
    email = models.EmailField(max_length=254,unique=True)
    password =  models.CharField(max_length=200)
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()
    usertype = models.CharField(max_length=20,choices=c)

# blog categories name here
# categories name inserted manually in table from MYSQL
class BCategories(models.Model):
    
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.id

# blog post details here 
class BPost(models.Model):
    
    Title = models.CharField(max_length=250)
    Image = models.ImageField(upload_to="uploads/blogimg/")
    Category = models.ForeignKey(BCategories,on_delete=models.CASCADE)
    Summary = models.CharField(max_length=255)
    content = models.TextField()
    username = models.ForeignKey(UserDetNew,on_delete=models.CASCADE)
    draft = models.BooleanField(default=False)
