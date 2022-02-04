from unicodedata import name
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[

        path('',index,name='index'),
        path('registers/',registers,name='register'),
        path('login/',loginpage,name='login'),
        path('loginact/',loginact,name='loginact'),
        path('logout/',logoutend,name='logoutall'),
        path('dashboard/',dashboard,name='dashboard'),
        path('addblog/',addblog,name='addblog'),
        path('viewblogcat/<int:catapk>/',viewblogcat,name='viewblogcat'),
]
