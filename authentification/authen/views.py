import os
from rest_framework.response import Response
from rest_framework import generics,status,views,permissions
from authen.serilaizers import EmailVerificationSerializer, LogoutSerializer, RegisterSerilaizer ,LoginSerializer, ResetPPasswordEmailSerializer, SetNewPasswordSerialize
from rest_framework_simplejwt.tokens import RefreshToken
from .renderers import UserRender
from .models import User
from .utlis import util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRender
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utlis import util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
# Create your views here.

class CustomerRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class RegisterView(generics.GenericAPIView):
    authentication_classes = []
    renderer_classes = (UserRender,)
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
        absurl = 'http://'+current_site +relativelink+'?token='+str(token)
        email_body = 'Hi ' +user.username+ ' use link below to verify your email \n '+absurl
        data = {'email_body':email_body,'email_to':user.email,'email_subject':'verify your email'}
        util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serilaizer = self.serializer_class(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        return Response(serilaizer.data,status=status.HTTP_200_OK)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)
        except  jwt.ExpiredSignatureError:
            return Response({'error':'Activation Expired'},status=status.HTTP_400_BAD_REQUEST)
        except  jwt.exceptions.DecodeError:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)



class PasswordRestEmail(generics.GenericAPIView):
    serializer_class = ResetPPasswordEmailSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativelink = reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            redirect_url = request.data.get('redirect_url','')
            absurl = 'http://'+current_site +relativelink
            email_body = 'Hello\n use link below to reset your password \n'+absurl+'?redirect_url='+redirect_url
            data = {'email_body':email_body,'email_to':user.email,'email_subject':'Reset your password '}
            util.send_email(data)
        return Response({'success':'We have sent you a link to reset your password'},status=status.HTTP_200_OK)

class PasswordTokenCheck(generics.GenericAPIView):
    serializer_class = ResetPPasswordEmailSerializer
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url')
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomerRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomerRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')
            if redirect_url and len(redirect_url) > 3:
                return CustomerRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomerRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')
        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomerRedirect(redirect_url+'?token_valid=False')       
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerialize
    def patch(self,request):
        serilaizer = self.serializer_class(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Password resert success'},status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
