# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect,render
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

# Create your views here.
def login(request):
    args ={}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/parser/href')
        else:
            args['login_error'] = "Пользователь не найден1"
            return render_to_response('login.html',args)

    else:
        return render_to_response('login.html', args)

def logout(request):
    auth.logout(request)
    return redirect("/parser/href")# Create your views here.


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],password=newuser_form.cleaned_data['password2'])
            auth.login(request,newuser)
            return redirect('/events/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html',args)
