from django.shortcuts import redirect, render
from django.http import request
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'userapp/index.html')

def registers(request):
    if request.method == "POST":
        
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['uname']
        imgs = request.FILES['imgs']
        email = request.POST['email']
        temppass = request.POST['pass']
        password =  request.POST['password']
        address =  request.POST['address']
        city =  request.POST['city']
        state =  request.POST['state']
        pincode = request.POST['pincode']
        utype = request.POST['usertypes']

        if password!=temppass:
            messages.add_message(request,messages.ERROR,"Password does not match!!")
        else:
            User.objects.create_user(username=username,password=password).save()
            lastobject = len(User.objects.all())-1
            UserDetNew(id=User.objects.all()[int(lastobject)].id,fname=fname,lname=lname,username=User.objects.all()[int(lastobject)].username,email=email,password=User.objects.all()[int(lastobject)].password,address=address,city=city,state=state,pincode=pincode,usertype=utype,profile_pic=imgs).save()
        
            fresult = "Details Stored Successfully!! Thank You"
        
            return render(request,'userapp/register.html',{'status':fresult})
    
    return render(request,'userapp/register.html')

def loginpage(request):
    return render(request,'userapp/login.html')

def loginact(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            current_user = request.user
            ids = current_user.id
            r = UserDetNew.objects.get(pk=ids)

            submenu = BCategories.objects.all()

            # identify usertype
            if r.usertype == 'Doctor':

                # assign type number to users
                context = {'type':1,'docdetails':UserDetNew.objects.filter(username = request.user.username),'submenu':submenu}
                return render(request,'userapp/dashboard.html',context)
            else:
                context1 = {'type':0,'patdetails':UserDetNew.objects.filter(username = request.user.username),'submenu':submenu}
                return render(request,'userapp/dashboard.html',context1)
        else:
            return redirect('login')

def logoutend(request):
    logout(request)
    return render(request,'userapp/login.html')

# doctor and patient main dashboard view
def dashboard(request):
    
    # blog categories name from database
    submenu = BCategories.objects.all()       
    
    current_user_id = request.user.id
    t = UserDetNew.objects.get(pk=current_user_id)
    if t.usertype == 'Doctor':
        # assign type number to user
        context = {'type':1,'docdetails':UserDetNew.objects.filter(username = request.user.username),'submenu':submenu}
    else:
        context = {'type':0,'patdetails':UserDetNew.objects.filter(username = request.user.username)}
    
    return render(request,'userapp/dashboard.html',context)


# doctor add blog page view
def addblog(request):

    if request.method=="POST":
        title = request.POST['title']
        imgs = request.FILES['bimgs']
        bcat = request.POST['bcategory']
        summary = request.POST['summary']
        content = request.POST['content']
        draft = request.POST.get('is_blog','0')  # handles multi key value dict error, default value is 0(0-means blog is not a draft)

        submenu = BCategories.objects.all()

        # get user selected category id
        bid = BCategories.objects.get(name=bcat).id

        uid = request.user.id  # get current logged in user id
        
        # store new blog details in DB
        BPost.objects.create(Title=title,Image=imgs,Summary=summary,content=content,Category_id=bid,username_id=uid,draft=draft).save()

        fresult = "Blog Post Created Successfully!!"
        return render(request,'userapp/addblog.html',{'status':fresult,'submenu':submenu})

    # if no post request just render the page
    submenu = BCategories.objects.all()
    return render(request,"userapp/addblog.html",{'submenu':submenu})


# doctor & patient view blog list page
def viewblogcat(request,catapk):                     # get patient or doctor selected blog category id
    
    submenu = BCategories.objects.all()

    current_user_id = request.user.id
    r = UserDetNew.objects.get(pk=current_user_id)  # details of current logged in user

    if r.usertype == 'Doctor':                        

        # get details from BPost table of the category id doc has selected
        details = BPost.objects.filter(Category_id=catapk,username_id=request.user.id)

        # check if doctor has posted any blog of the category he has selected 
        if BPost.objects.filter(Category_id=catapk,username_id=request.user.id).exists():
            return render(request,'userapp/viewblog.html',{'type':1,'blogdet':details,'submenu':submenu})
        
        # if no blogs posted by the doc of the selected category
        else:
            context = {'msg':'No Blog Post Available!!!','type':1,'docdetails':UserDetNew.objects.filter(username = request.user.username),'submenu':submenu}
            return render(request,'userapp/dashboard.html',context)
    
    else:

        # get details from BPost table of the category id patient has selected with blog type not marked as draft
        details = BPost.objects.filter(Category_id=catapk,draft=0)

        # if above queryset has anything to print 
        if  BPost.objects.filter(Category_id=catapk,draft=0).exists():
            return render(request,'userapp/viewblog.html',{'type':0,'submenu':submenu,'blogdet':details})
        
        # if no blog post available of the selected category id
        else:
            context = {'msg':'No Blog Post Available!!!','type':0,'patdetails':UserDetNew.objects.filter(username = request.user.username),'submenu':submenu}
            return render(request,'userapp/dashboard.html',context)


