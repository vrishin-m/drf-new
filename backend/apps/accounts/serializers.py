from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "full_name" ]



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only= True
    )

    class Meta:
        model= Account
        fields=[
            "email",
            "full_name",
            "password",
        ]

    def validate_email(self,value):
        if Account.objects.filter(
            email=value
        ).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )
        return value 
    
    def create(self , validated_data):
        return Account.objects.create_user(
            **validated_data
        )