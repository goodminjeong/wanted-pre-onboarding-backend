from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "is_active",
            "is_admin",
            "last_login",
        )

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


class SigninSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError("비밀번호를 다시 확인해 주십시오.")
        else:
            raise serializers.ValidationError("존재하지 않는 이메일입니다.")

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            "refresh": refresh,
            "access": access,
        }

        return data
