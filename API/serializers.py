from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile,Vidoe
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

class BasicProfileInfo(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['id']

class UserInfoSerializer(serializers.ModelSerializer):
	profile =  BasicProfileInfo()
	class Meta:
		model = User
		fields =['id','username','profile'] 
# Vidoes =====================================================

class VidoeSerializer(serializers.ModelSerializer):
	number_of_voter =  serializers.SerializerMethodField()
	voted_by_req_user = serializers.SerializerMethodField()
	user = UserInfoSerializer()
	class Meta:
		model = Vidoe
		fields = '__all__' 

	def get_number_of_voter(self,obj):
		if obj.number_of_voter.count():
			return obj.number_of_voter.count()
		else:
			return 0

	def get_voted_by_req_user(self, obj):
		user = self.context['request'].user
		print(user)
		return user in obj.number_of_voter.all()

# Profile ================================================
class UserProfileSerializer(serializers.ModelSerializer):
	user= serializers.SerializerMethodField()
	point = serializers.SerializerMethodField()
	ranking = serializers.SerializerMethodField()
	class Meta:
		model = Profile
		fields = '__all__'
	def get_user(self,obj):
		return obj.user.username
	def get_point(self,obj):
		user_vidoes = Vidoe.objects.filter(user = obj.user)
		result = 0
		for vidoe in user_vidoes:
			result = result + vidoe.number_of_voter.count()
		return result

	# def get_ranking(self,obj):
	# 	users = Profile.objects.all()
	# 	users_points = users.point
	# 	print(users_points)

	