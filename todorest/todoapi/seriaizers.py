#serializer ,
#modelserializer
from django.core.serializers import serialize
from rest_framework import serializers
from .models import Todo
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
class TodoSerializer(ModelSerializer):
    class Meta:
        model=Todo
        fields=["task_name","status","user"]


class UserCreationSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","username","email","password"]



    #
    # def validate(self, attrs):

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data["username"],
                                        first_name=validated_data["first_name"],
                                        email=validated_data["email"],
                                        password=validated_data["password"])


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
