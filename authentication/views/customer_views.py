from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from sequences import get_next_value

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.models import Customer, User
from authentication.serializers import CustomerSerializer, CustomerListSerializer
from authentication.filters import CustomerFilter
from authentication.decorators import has_permissions

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
	request=CustomerSerializer,
	responses=CustomerSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllCustomer(request):
	customers = Customer.objects.all()
	total_elements = customers.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	customers = pagination.paginate_data(customers)

	serializer = CustomerListSerializer(customers, many=True)

	response = {
		'customers': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	request=CustomerSerializer,
	responses=CustomerSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllCustomerWithoutPagination(request):
	customers = Customer.objects.all()

	serializer = CustomerListSerializer(customers, many=True)

	return Response({'customers': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PRODUCT_DETAILS.name])
def searchCustomer(request):

	customers = CustomerFilter(request.GET, queryset=Customer.objects.all())
	customers = customers.qs

	print('customers: ', customers)

	total_elements = customers.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	customers = pagination.paginate_data(customers)

	serializer = CustomerListSerializer(customers, many=True)

	response = {
		'customers': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(customers) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no customers matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS.name])
def getACustomer(request, pk):
	try:
		customer = Customer.objects.get(pk=pk)
		serializer = CustomerListSerializer(customer)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Customer id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createCustomer(request):
	data = request.data
	print('data: ', data)

	customer_data_dict = {}

	current_datetime = timezone.now()
	current_datetime = str(current_datetime)
	print('current_datetime str: ', current_datetime)
		
	for key, value in data.items():
		if value != '' and value != 0 and value != '0' and value != 'undefined':
			customer_data_dict[key] = value

	first_name = customer_data_dict.get('first_name', 'random')
	username = customer_data_dict.get('username', None)
	email = customer_data_dict.get('email', None)
	primary_phone = customer_data_dict.get('primary_phone', None)

	if not username:
		username = str(first_name) + str(get_next_value('sequential_user'))
		customer_data_dict['username'] = username

	email_token = uuid.uuid4().hex
	phone_otp = random.randint(123456, 987654)

	customer_data_dict['email_token'] = str(email_token)
	customer_data_dict['phone_otp'] = phone_otp
	customer_data_dict['last_login'] = current_datetime
	customer_data_dict['user_type'] = 'customer'

	serializer = CustomerSerializer(data=customer_data_dict, many=False)

	if serializer.is_valid():
		serializer.save()
		return Response({'detail': "signup successfull."}, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateCustomer(request, pk):
	data = request.data
	print('customer data: ', data)
	print('content_type: ', request.content_type)
	filtered_data = {}
	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	print('filtered_data: ', filtered_data)

	image = filtered_data.get('image', None)
	
	try:
		customer = Customer.objects.get(pk=int(pk))
	except ObjectDoesNotExist:
		return Response({'detail': f"Customer id - {pk} doesn't exists"})

	if type(image) == str and image is not None:
		poped_image = filtered_data.pop('image')

	serializer = CustomerSerializer(customer, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	



@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteCustomer(request, pk):
	try:
		customer = Customer.objects.get(pk=pk)
		ledger = LedgerAccount.objects.get(reference_id=customer.id)
		ledger.delete()
		customer.delete()
		return Response({'detail': f'Customer id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Customer id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


