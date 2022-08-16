from rest_framework import serializers
from .models import Income
class IncomeSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['date','id','description','amount','source']