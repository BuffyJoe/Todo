from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import ToDo
from .forms import CreateToDo, ToDoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='log-in')
def index(request):
    activities = ToDo.objects.filter(owner=request.user).order_by('-end')
    today = timezone.localtime(timezone.now())
    todo = ToDo.objects.filter(owner=request.user).count()
    complete = ToDo.objects.filter(completed=True, owner=request.user).count()
    percent = complete * 100 // todo
    # expired = ToDo.objects.expired()
    if request.method == 'POST':
        try:
            search = request.POST.get('todo')
            activities = ToDo.objects.filter(todo__icontains=search, owner=request.user).order_by('-end')
            todo = activities.count()
            complete = activities.filter(completed=True, owner=request.user).count()
            try:
                percent = complete * 100 // todo
            except:
                return redirect('home')
            
        except:
            search = request.POST.get('end')
            activities = ToDo.objects.filter(end=search, owner=request.user).order_by('-end')
            todo = activities.filter(owner=request.user).count()
            complete = activities.filter(completed=True, owner=request.user).count()
            try:
                percent = complete * 100 // todo
            except:
                return redirect('home')
    today = timezone.localtime(timezone.now())
    expiredd = ToDo.objects.filter(end=today, owner=request.user)
    if expiredd:
        expiredd.update(expired=True)
    
 
    context = {
        'activities' : activities,
        'percent' : percent,
        'today' : today,
        # 'expired': expired,
    }
    return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            return render(request, 'home.html', {})
    return render(request, 'sign-up.html', {})
    
def edit(request, pk):
     todo = ToDo.objects.get(id=pk)
     form = ToDoForm(instance=todo)
     if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect('home')
     context = {
         'form': form,
     }
     return render(request, 'edit.html', context)

def progress(request):
    today = timezone.localtime(timezone.now())
    activities = ToDo.objects.filter(end=today, owner=request.user)
    if activities:
        activities.update(expired=True)
    context = {
        'activities' : activities,
        'today' : today, 
    }
    return render(request, 'percent.html', context)
    
def create(request):
     form = CreateToDo()
     if request.method == 'POST':
        form = CreateToDo(request.POST)
        if form.is_valid():
          form = form.save(commit=False)
          form.owner = request.user
          form.save()
          return redirect('home')
     context = {
         'form': form, 
        }
     return render(request, 'create.html', context)
def deletetask(request, pk):
    obj = ToDo.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    
    context = {

    }
    return render(request, 'delete.html', context)
def expiring(request):
    today = timezone.localtime(timezone.now())
    activities = ToDo.objects.filter(end = today, completed=False, expired=False, owner=request.user)
    all = ToDo.objects.filter(end=today, owner=request.user)
    todo = ToDo.objects.filter(end = today, owner=request.user).count()
    complete = ToDo.objects.filter(completed=True, end = today, owner=request.user).count()
    try:
        percent = complete * 100 // todo
    except:
        percent = 0
    
    context = {
        'today' : today,
        'activities' : activities,
        'all_activities' : all,
        'percent' : percent
    }
    return render(request, 'expiring.html', context)

    
def Loginpage(request): 
     if request.user.is_authenticated:
          return redirect('home')
     if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')

          try:
               user = User.objects.get(username=username)
          except:
               messages.error(request, 'User does not exist')

          user = authenticate(request, username=username, password=password) 
          if user is not None:
               login(request, user)
               return redirect('home')
     
     context = {'login' : True}
     return render(request, 'login.html', context)
     
def logoutpage(request):
     if request.method == 'POST':
          logout(request)
          return redirect('home')
     return render(request, 'login.html', {'logout' : True})


def register(request):
     if request.user.is_authenticated:
          return redirect('home')
     form = UserCreationForm()
     if request.method == 'POST':
          form = UserCreationForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.username = user.username.lower()
               user.save()
               login(request, user)
               return redirect('home')
     return render(request, 'register.html', {'form' : form})


