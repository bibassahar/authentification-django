from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView,)

from authen import views

urlpatterns=[
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('verify-email/',views.VerifyEmail.as_view(),name='verify-email'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
    path('request-reset-email/',views.PasswordRestEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheck.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/',views.SetNewPasswordApiView.as_view(), name='password-reset-complete')

]