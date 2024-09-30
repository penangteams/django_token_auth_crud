from rest_framework import serializers
from .models import User, Jobseeker, Owner, Employer
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password", "isActive"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class JobseekerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)

    class Meta:
        model = Jobseeker
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        j_seeker = Jobseeker.objects.create(user=user, **validated_data)
        return j_seeker


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)

    class Meta:
        model = Owner
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        ownr = Owner.objects.create(user=user, **validated_data)
        return ownr


class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)

    class Meta:
        model = Employer
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        eployer = Employer.objects.create(user=user, **validated_data)
        return eployer


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User

    fields = ["id", "password"]


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    def validate_the_password(self, value):
        validate_password(value)
        return value
