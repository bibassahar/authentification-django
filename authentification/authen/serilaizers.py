from rest_framework import serializers
from authen.models import User 

class RegisterSerilaizer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120,min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']
    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError('The user name should contains only alphanumeric charcters')
        return attrs
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
