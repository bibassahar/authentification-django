from rest_framework import serializers
from .models import Expense
class ExpenseSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['date','id','description','amount','category']