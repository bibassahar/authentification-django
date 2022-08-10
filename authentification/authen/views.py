import email
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from authen.serilaizers import RegisterSerilaizer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utlis import util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# Create your views here.
class RegisterView(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerilaizer
    def post(self,request):
        user = request.data
        serilaizer = self.serializer_class(data=user)
        serilaizer.is_valid(raise_exception=True)
        serilaizer.save()
        user_data = serilaizer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativelink = reverse('verify-email')
        absurl = 'http/'+current_site +relativelink+'?token='+str(token)
        email_body = 'Hi ' +user.username+ ' Use link below to verify your email \n '+absurl
        data = {'email_body':email_body,'email_to':user.email,'email_subject': 'verify your email',}
        util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass


