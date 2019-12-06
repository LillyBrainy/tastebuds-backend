
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import (UserCreateSerializer , UserLoginSerializer ,VidoeSerializer,UserProfileSerializer,UserInfoSerializer)
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView,RetrieveUpdateAPIView
from .models import Profile,Vidoe
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
import random

class UserCreateApiView(CreateAPIView):
	serializer_class = UserCreateSerializer
	

class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer

	def post(self, request):
		my_data = request.data
		serializer = UserLoginSerializer(data=my_data)
		if serializer.is_valid(raise_exception=True):
			valid_data = serializer.data
			return Response(valid_data, status=HTTP_200_OK)
		return Response(serializer.errors, HTTP_400_BAD_REQUEST)

class UserBasicInfo(RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class=UserInfoSerializer
	lookup_fields = 'id'
	lookup_url_kwarg = 'user_id'

# Vidoes ================================

class CreateVidoeAPIView(CreateAPIView):
	serializer_class = VidoeSerializer
	def perform_create(self, serializer):
		if self.request.user.is_authenticated:
			serializer.save(user=self.request.user)
		else:
			print('none')		

class FilterVidoeSerializer(ListAPIView):
	serializer_class = VidoeSerializer
	def get_queryset(self):
		category = self.kwargs['category']
		return Vidoe.objects.filter(category=category)

class FilterUserVidoeSerializer(ListAPIView):
	serializer_class = VidoeSerializer
	def get_queryset(self):
		user = self.kwargs['user_id']
		return Vidoe.objects.filter(user=user)

class PickTwoVidoesRandomelyAPIView(ListAPIView):
	serializer_class = VidoeSerializer
	def get_queryset(self):
		# num_vidoes = Vidoe.objects.all().order_by('?')[:2]
		# rand_vidoes = random.Random().sample(range(num_vidoes), 2)
		# print(rand_vidoes)
		category = self.kwargs['category']
		return  Vidoe.objects.filter(category=category).order_by('?')[:2]

class LikeVidoeAPIView(APIView):
	def get(self, request, format=None, vidoe_id=None):

		vidoe = Vidoe.objects.get(id=vidoe_id)
		user = self.request.user
		if user.is_authenticated:
			if user in vidoe.number_of_voter.all():
				vote =  False
				vidoe.number_of_voter.remove(user)
			else:
				vote=True
				vidoe.number_of_voter.add(user)
		
		data = {
			'vote': vote
		        }		
		return Response(data, status=status.HTTP_200_OK)

# Profile ==========================================

class UserProfileAPIView(RetrieveAPIView):
	queryset = Profile.objects.all()
	serializer_class = 	UserProfileSerializer
	lookup_fields = 'id'
	lookup_url_kwarg = 'profile_id'
	


