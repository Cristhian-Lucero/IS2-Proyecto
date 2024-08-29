from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, "login/login.html")

def base(request):
    return render(request, "login/base.html")

def base2(request):
    return render(request, "login/base2.html")