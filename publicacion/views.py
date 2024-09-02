from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
#from .forms import *


# Create your views here.

def home(request):
    return render(request, 'homepage/home.html')