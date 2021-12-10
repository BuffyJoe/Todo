from django.db.models import fields
from django.forms.models import ModelForm, modelform_factory
from .models import ToDo
from app import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['todo', 'end', 'completed', 'description']

class CreateToDo(ModelForm):
    class Meta:
        model = ToDo
        fields = ['todo', 'end', 'description']

class registerform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']