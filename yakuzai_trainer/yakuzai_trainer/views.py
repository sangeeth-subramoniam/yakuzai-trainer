from django.shortcuts import render, redirect

def home(request):
    print('Entering homepage')
    return redirect('train:train_home')