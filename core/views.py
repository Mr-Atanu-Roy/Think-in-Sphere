from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    
    return render(request, './core/home.html')