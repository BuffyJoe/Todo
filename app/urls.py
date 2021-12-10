from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('exp/', views.expiring, name="exp"),
    path('delete/<int:pk>', views.deletetask, name='delete'),
    path('create/', views.create, name='create'),
    path('log-out/', views.logoutpage, name='log-out'),
    path('log-in/', views.Loginpage, name='log-in'),
    path('sign-up/', views.register, name='sign-up')
]
