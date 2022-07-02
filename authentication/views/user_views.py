# from _typeshed import ReadableBuffer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

from rest_framework import serializers, status
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import OpenApiParameter, extend_schema

from authentication.decorators import has_permissions
from authentication.models import Permission
from authentication.serializers import (AdminUserSerializer, PasswordChangeSerializer, AdminUserListSerializer)
from authentication.filters import UserFilter

from commons.enums import AuthPermEnum
from commons.pagination import Pagination




# Create your views here.
User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super().validate(attrs)

		# data['username'] = self.user.username
		# data['email'] = self.user.email

		serializer = AdminUserListSerializer(self.user).data

		for k, v in serializer.items():
			data[k] = v

		# data.pop('refresh')
		# data.pop('access')
		return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=AdminUserSerializer,
	responses=AdminUserSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_LIST.name])
def getAllUser(request):
	users = User.objects.all()
	total_elements = users.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	users = pagination.paginate_data(users)

	serializer = AdminUserListSerializer(users, many=True)

	response = {
		'users': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=AdminUserSerializer,
	responses=AdminUserSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_LIST.name])
def getAllUserWithoutPagination(request):
	users = User.objects.all()

	serializer = AdminUserListSerializer(users, many=True)

	return Response({'users': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=AdminUserSerializer, responses=AdminUserSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_DETAILS.name])
def getAUser(request, pk):
	try:
		user = User.objects.get(pk=pk)
		serializer = AdminUserSerializer(user)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=AdminUserListSerializer, responses=AdminUserListSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_LIST.name])
def searchUser(request):
	users = UserFilter(request.GET, queryset=User.objects.all())
	users = users.qs

	print('searched_products: ', users)

	total_elements = users.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	users = pagination.paginate_data(users)

	serializer = AdminUserListSerializer(users, many=True)

	response = {
		'users': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(users) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no users matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=AdminUserSerializer, responses=AdminUserSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_CREATE.name])
def createUser(request):
	data = request.data

	current_datetime = timezone.now()
	current_datetime = str(current_datetime)
	print('current_datetime str: ', current_datetime)

	user_data_dict = {}

	for key, value in data.items():
		user_data_dict[key] = value
		
	user_data_dict['last_login'] = current_datetime

	print('user_data_dict: ', user_data_dict)

	serializer = AdminUserSerializer(data=user_data_dict, many=False)
	
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=AdminUserSerializer, responses=AdminUserSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_UPDATE.name, AuthPermEnum.USER_PARTIAL_UPDATE.name])
def updateUser(request, pk):
	try:
		user = User.objects.get(pk=pk)
		data = request.data
		serializer = AdminUserSerializer(user, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=AdminUserSerializer, responses=AdminUserSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_DELETE.name])
def deleteUser(request, pk):
	try:
		user = User.objects.get(pk=pk)
		user.delete()
		return Response({'detail': f'User id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)





@extend_schema(request=PasswordChangeSerializer)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_UPDATE, AuthPermEnum.USER_PARTIAL_UPDATE])
def userPasswordChange(request, pk):
	try:
		user = User.objects.get(pk=pk)
		data = request.data
		password = data['password']
		confirm_password = data['confirm_password']

		if password == confirm_password:
			user.password = make_password(password)
			user.save()
			response = {'detail': f"User Id  {pk}'s password has been changed successfully."}
			return Response(response, status=status.HTTP_200_OK)
		else:
			response = {'detail': f"Password does not match."}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		response = {'detail': f"User id - {pk} doesn't exists"}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
@has_permissions([AuthPermEnum.USER_UPDATE, AuthPermEnum.USER_PARTIAL_UPDATE])
def userImageUpload(request, pk):
	try:
		user = User.objects.get(pk=pk)
		data = request.data
		# image = 
		if 'image' in data:
			print( "================>" ,data, data['image'], type(data['image']))
			user.image = data['image']
			user.save()
			return Response(user.image.url, status=status.HTTP_200_OK)
		else:
			response = {'detail': f"Please upload a valid image"}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		response = {'detail': f"User id - {pk} doesn't exists"}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)




