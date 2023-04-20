from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Profile, Task, Goal, Quota
from django.utils import timezone
import json


# Create your views here.
def index(request):
    return render(request, 'app/index.html')


def registerPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                auth.login(request, user)
                return redirect('info')
        else:
            messages.info(request, 'Password mismatch')
            return redirect('register')
    else:
        return render(request, 'app/registerPage.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'app/loginPage.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='login')
def info(request):
    if request.method == 'POST':
        name = request.POST['fullname']
        designation = request.POST['designation']
        profile = Profile(user=request.user, name=name, designation=designation)
        profile.save()
        return redirect('dashboard')
    else:
        return render(request, 'app/info.html')


def returnDate(x):
    return int(x.strftime("%d"))

@login_required(login_url='login')
def dashboard(request):
    month = timezone.now().month
    tasks = Task.objects.filter(user=request.user)
    goals = Goal.objects.filter(user=request.user)
    sleep = list(Quota.objects.filter(user=request.user).values_list('sleep', flat=True))[-7:]
    sleepTime = list(Quota.objects.filter(user=request.user).values_list('date', flat=True))[-7:]
    date = list(map(returnDate, sleepTime))
    studyHrs = list(Quota.objects.filter(user=request.user).values_list('study', flat=True))[-7:]
    context = {'tasks': tasks, 'goals': goals, 'sleep': sleep, 'date': date, 'study':studyHrs}

    if request.method == 'POST' and 'taskname' in request.POST:
        name = request.POST['taskname']
        time = request.POST['time']
        task = Task(user=request.user, name=name, time=time)
        task.save()
        return redirect('dashboard')
    
    if request.method == 'POST' and 'goalname' in request.POST:
        name = request.POST['goalname']
        goal = Goal(user=request.user, name=name)
        goal.save()
        return redirect('dashboard')

    if request.method=='POST' and ('sleep' in request.POST or 'study' in request.POST):
        sleep = request.POST['sleep']
        study = request.POST['study']
        if Quota.objects.filter(date=timezone.now().date()).exists():
            messages.info(request, 'You have already entered your sleep and study quota for today')
            return redirect('dashboard')
        else:
            quota = Quota(user=request.user, sleep=sleep, study=study)
            quota.save()
            return redirect('dashboard')
        
    if request.method == 'POST' and 'update_task_status' in request.POST:
        task_ids = request.POST.getlist('task_checkbox')
        for task_id in task_ids:
            task = Task.objects.get(id=task_id)
            task.delete()
        return redirect('dashboard')
    
    if request.method == 'POST' and 'update_goal_status' in request.POST:
        goal_ids = request.POST.getlist('goal_checkbox')
        for goal_id in goal_ids:
            goal = Goal.objects.get(id=goal_id)
            goal.delete()
        return redirect('dashboard')

    else:
        return render(request, 'app/dashboard.html', context)
