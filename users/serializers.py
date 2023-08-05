from rest_framework import serializers
from rest_framework import serializers
from users.models import User
from rest_framework.generics import get_object_or_404


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "is_active")

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if "password" in validated_data.keys():
            password = validated_data.pop("password")
            user.set_password(password)
        user.save()
        return user
