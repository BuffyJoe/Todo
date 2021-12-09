from django.db.models import fields
from django.forms.models import ModelForm, modelform_factory
from .models import ToDo
from app import models

class ToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['todo', 'end', 'completed', 'description']

class CreateToDo(ModelForm):
    class Meta:
        model = ToDo
        fields = ['todo', 'end', 'description']