from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class ToDoManager(models.Manager):
#     def active(self):
#         return self.exclude(end__lt=today().date)

#     def expired(self):
#         return self.filter(end__lt=today().date)


class ToDo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    end = models.DateField()
    start = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    
    # objects = ToDoManager()

    def __str__(self):
        return f'{self.owner} - {self.todo}'