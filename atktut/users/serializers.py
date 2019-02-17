from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'email')
        read_only_fields = ('username', )


class CreateUserSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     username = attrs.get("username")
    #     first_name = attrs.get("first_name")
    #     last_name = attrs.get("last_name")
    #     email = attrs.get("email")
    #     password = attrs.get("password")
    #     confirm = attrs.get("confirm")

    #     return super().validate(attrs)

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'auth_token',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
