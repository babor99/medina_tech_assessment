from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from sequences import get_next_value

from account.models import Group, LedgerAccount

from authentication.models import User, Vendor
from authentication.serializers import VendorSerializer, VendorListSerializer
from authentication.filters import VendorFilter
from authentication.decorators import has_permissions
from authentication.utils import send_phone_otp, send_verification_email

from commons.pagination import Pagination
from commons.enums import PermissionEnum

import uuid
import random



# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=VendorSerializer,
	responses=VendorSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllVendor(request):
	vendors = Vendor.objects.all()
	total_elements = vendors.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	vendors = pagination.paginate_data(vendors)

	serializer = VendorListSerializer(vendors, many=True)

	response = {
		'vendors': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	request=VendorSerializer,
	responses=VendorSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllVendorWithoutPagination(request):
	vendors = Vendor.objects.all()

	serializer = VendorListSerializer(vendors, many=True)

	return Response({'vendors': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=VendorSerializer, responses=VendorSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS.name])
def getAVendor(request, pk):
	try:
		vendor = Vendor.objects.get(pk=pk)
		serializer = VendorListSerializer(vendor)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Vendor id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=VendorSerializer, responses=VendorSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchVendor(request):
	vendors = VendorFilter(request.GET, queryset=Vendor.objects.all())
	vendors = vendors.qs

	print('searched_products: ', vendors)

	total_elements = vendors.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	vendors = pagination.paginate_data(vendors)

	serializer = VendorListSerializer(vendors, many=True)

	response = {
		'vendors': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(vendors) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no vendor matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=VendorSerializer, responses=VendorSerializer)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createVendor(request):
	data = request.data

	print('data :', data) 

	vendor_data_dict = {}

	current_datetime = timezone.now()
	current_datetime = str(current_datetime)
	print('current_datetime str: ', current_datetime)

	try:
		group_obj = Group.objects.get(name='Sundry Creditors')
	except Group.ObjectDoesNotExist:
		return Response("Please insert a 'Purchase Accounts' data in the Group table and then try again")

	for key, value in data.items():
		if value != '' and value != 0 and value != '0' and value != 'undefined':
			vendor_data_dict[key] = value

	first_name = vendor_data_dict.get('first_name', 'random')
	username = vendor_data_dict.get('username', None)
	email = vendor_data_dict.get('email', None)
	primary_phone = vendor_data_dict.get('primary_phone', None)

	if not username:
		username = str(first_name) + str(get_next_value('sequential_user'))
		vendor_data_dict['username'] = username

	email_token = uuid.uuid4().hex
	phone_otp = random.randint(123456, 987654)

	vendor_data_dict['email_token'] = email_token
	vendor_data_dict['phone_otp'] = phone_otp
	vendor_data_dict['last_login'] = current_datetime
	vendor_data_dict['user_type'] = 'vendor'

	print('vendor_data_dict: ', vendor_data_dict)

	serializer = VendorSerializer(data=vendor_data_dict, many=False)

	if serializer.is_valid():
		otp_res = send_phone_otp(primary_phone, phone_otp)
		print('otp_res: ', otp_res)
		print('typeof otp_res: ', type(otp_res))
		if otp_res['message'] == 'Success!' and otp_res['isError'] == False:

			serializer.save()

			send_verification_email(email, email_token)

			id = serializer.data['id']
			vendor_ledger_obj = LedgerAccount.objects.create(name=username, ledger_type='vendor_ledger', reference_id=id, head_group=group_obj)
			print('vendor_ledger_obj: ', vendor_ledger_obj)

			return Response({'detail': f"OTP sent"}, status=status.HTTP_200_OK)
		else:
			return Response({'detail': f"Your phone number is invalid!"}, status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=VendorSerializer, responses=VendorSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateVendor(request,pk):
	data = request.data
	print('vendor data: ', data)
	print('content_type: ', request.content_type)
	filtered_data = {}
	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	print('filtered_data: ', filtered_data)

	image = filtered_data.get('image', None)
	
	try:
		vendor = Vendor.objects.get(pk=int(pk))
	except ObjectDoesNotExist:
		return Response({'detail': f"Customer id - {pk} doesn't exists"})

	if type(image) == str and image is not None:
		poped_image = filtered_data.pop('image')
		serializer = VendorSerializer(vendor, data=filtered_data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors)
	else:
		serializer = VendorSerializer(vendor, data=filtered_data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=VendorSerializer, responses=VendorSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteVendor(request, pk):
	try:
		vendor = Vendor.objects.get(pk=pk)
		ledger = LedgerAccount.objects.get(reference_id=vendor.id)
		ledger.delete()
		vendor.delete()
		return Response({'detail': f'Vendor id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Vendor id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


