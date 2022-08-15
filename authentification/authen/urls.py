from django.urls import path
from authen import views

urlpatterns=[
    path('register/',views.RegisterView.as_view(),name='register'),
    path('verify-email/',views.VerifyEmail.as_view(),name='verify-email'),
    path('login/',views.LoginApiView.as_view(),name='login'),

]