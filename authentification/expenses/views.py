from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView
from .models import Expense
from .serilaizers import ExpenseSerilaizer
from rest_framework import permissions
from .permissions import IsOwner
# Create your views here.

class ExpenseList(ListCreateAPIView):
    serializer_class = ExpenseSerilaizer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class ExpenseDetailApiView(RetrieveUpdateAPIView):
    serializer_class = ExpenseSerilaizer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    