from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from authen.serilaizers import RegisterSerilaizer
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
        return Response(user_data,status=status.HTTP_201_CREATED)
