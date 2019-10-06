from rest_framework import serializers
# from versatileimagefield.serializers import VersatileImageFieldSerializer

from atktut.course.serializers import ProgressDetailSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    progress = ProgressDetailSerializer(many=True, read_only=True)
    # headshot = VersatileImageFieldSerializer(
    #     sizes=[
    #         ('full_size', 'url'),
    #         ('avatar', 'crop__200x200'),
    #         ('small_square_crop', 'crop__50x50')
    #     ],
    #     required=False
    # )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'id', 'location',
                  'tagline', 'phone', 'email', 'dob', 'gender', 'progress', )
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
