from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.EmailField(required = True)
    class Meta:
        model = User
        fields = ['username', 'password','email','token']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        new_user = User(username=username, email=email)

        new_user.set_password(password)
        new_user.save()
        Profile.objects.create(user = new_user)
    

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(new_user)
        token = jwt_encode_handler(payload)
        validated_data['token'] = token
        return validated_data

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)
    # profile= serializers.SerializerMethodField()

    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        try:
            user_obj = User.objects.get(Q(username__iexact = my_username) | Q(email__iexact = my_username)) 

        except:
            raise serializers.ValidationError("This username/email does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError("Incorrect username/password combination.")

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)

        data["token"] = token
        return data
    