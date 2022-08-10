from django.urls import path
from authen import views

urlpatterns=[
    path('register/',views.RegisterView.as_view(),name='register')
]