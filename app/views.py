from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Profile, Task, Goal, Quota


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
            return redirect('/')
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


@login_required(login_url='login')
@csrf_exempt
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    goals = Goal.objects.filter(user=request.user)
    if request.method == 'POST':
        sleepHours = request.POST.get('sleep')
        return HttpResponse('Success')
    else:
        return render(request, 'app/dashboard.html', {'tasks': tasks, 'goals': goals})


@login_required(login_url='login')
def add_task(request):
    if request.method == 'POST':
        name = request.POST['taskname']
        time = request.POST['time']
        task = Task(user=request.user, name=name, time=time)
        task.save()
        return redirect('dashboard')
    else:
        return render(request, 'app/add-task.html')


@login_required(login_url='login')
def add_goal(request):
    if request.method == 'POST':
        name = request.POST['goalname']
        goal = Goal(user=request.user, name=name)
        goal.save()
        return redirect('dashboard')
    else:
        return render(request, 'app/add-goal.html')
