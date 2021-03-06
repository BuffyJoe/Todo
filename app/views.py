from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import ToDo
from .forms import CreateToDo, ToDoForm, registerform
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='log-in')
def index(request):
    activities = ToDo.objects.filter(owner=request.user).order_by('-end')
    today = timezone.localtime(timezone.now())
    todo = ToDo.objects.filter(owner=request.user).count()
    complete = ToDo.objects.filter(completed=True, owner=request.user).count()
    try:
        percent = complete * 100 // todo
    except:
        percent = 0
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
    expiredd = ToDo.objects.filter(end__lt=today, owner=request.user)
    if expiredd:
        expiredd.update(expired=True)
    
 
    context = {
        'activities' : activities,
        'percent' : percent,
        'today' : today,
        # 'expired': expired,
    }
    return render(request, 'home.html', context)
    
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
def create(request):
     form = CreateToDo()
     today = timezone.localtime(timezone.now())
     context = {
         'form': form, 
        }
     if request.method == 'POST':
        form = CreateToDo(request.POST)
        date = request.POST.get('end')
        try:
            if date < str(today):
                messages.error(request, 'set future date')
                return render(request, 'create.html', context)
        except:
            pass
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            messages.success(request, 'task added')
            # return redirect('home')
        else:
            messages.error(request, 'invalid task')
     return render(request, 'create.html', context)
def deletetask(request, pk):
    obj = ToDo.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    
    context = {
            'obj' : obj
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
    context = {'login' : True}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            pass

        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'incorrect Username or password')
            
    return render(request, 'login.html', context)
     
def logoutpage(request):
     if request.method == 'POST':
          logout(request)
          return redirect('home')
     return render(request, 'login.html', {'logout' : True})


def register(request):
    if request.user.is_authenticated:
          return redirect('home')
    form = registerform()
    if request.method == 'POST':
        form = registerform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)              
            return redirect('home')
        else:
            message = messages.error(request, 'error occured while submitting form')
            return render(request, 'register.html', {'form' : form, 'message' : message})
    return render(request, 'register.html', {'form' : form})


