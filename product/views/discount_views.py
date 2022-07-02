import datetime
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from product.models import Discount
from product.serializers import DiscountSerializer, DiscountListSerializer
from product.filters import DiscountFilter

from commons.pagination import Pagination
from commons.enums import ProductPermEnum




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=DiscountSerializer,
	responses=DiscountSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.DISCOUNT_LIST.name])
def getAllDiscount(request):
	_discounts = Discount.objects.all()
	total_elements = _discounts.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	_discounts = pagination.paginate_data(_discounts)

	serializer = DiscountListSerializer(_discounts, many=True)

	response = {
		'_discounts': serializer.data,
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
	request=DiscountSerializer,
	responses=DiscountSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.DISCOUNT_LIST.name])
def getAllDiscountWithoutPagination(request):
	discounts = Discount.objects.all()

	serializer = DiscountListSerializer(discounts, many=True)

	return Response({'discounts': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=DiscountSerializer,
	responses=DiscountSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.DISCOUNT_DETAILS.name])
def getADiscountByProductId(request, product_id):
	try:
		discount = Discount.objects.get(product__id=product_id)
		serializer = DiscountListSerializer(discount)
		return Response({'discounts': serializer.data}, status=status.HTTP_200_OK)
	except Discount.DoesNotExist:
		return Response({'detail': f"Discount doesn't exists with product id {product_id}"}, status=status.HTTP_400_BAD_REQUEST)





@extend_schema(request=DiscountSerializer, responses=DiscountSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.DISCOUNT_DETAILS.name])
def getADiscount(request, pk):
	try:
		discount = Discount.objects.get(pk=pk)
		serializer = DiscountListSerializer(discount)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Discount id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DiscountSerializer, responses=DiscountSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.DISCOUNT_LIST.name])
def searchDiscount(request):
	discounts = DiscountFilter(request.GET, queryset=Discount.objects.all())
	discounts = discounts.qs

	print('searched_products: ', discounts)

	total_elements = discounts.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	discounts = pagination.paginate_data(discounts)

	serializer = DiscountListSerializer(discounts, many=True)

	response = {
		'discounts': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(discounts) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no discounts matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=DiscountSerializer, responses=DiscountSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.DISCOUNT_CREATE.name])
def createDiscount(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	date_dict = {}

	date_dict['start_date'] = filtered_data.get('start_date', None)
	date_dict['end_date'] = filtered_data.get('end_date', None)

	print('date_dict: ', date_dict)

	current_time = datetime.datetime.now().time()

	for key, value in date_dict.items():
		if value is not None:
			date_time = str(value) + 'T' + str(current_time)
			filtered_data[key] = date_time

	serializer = DiscountSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DiscountSerializer, responses=DiscountSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.DISCOUNT_UPDATE.name])
def updateDiscount(request, pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	try:
		discount = Discount.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"Discount id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
	date_dict = {}

	date_dict['start_date'] = filtered_data.get('start_date', None)
	date_dict['end_date'] = filtered_data.get('end_date', None)

	print('date_dict: ', date_dict)

	current_time = datetime.datetime.now().time()

	for key, value in date_dict.items():
		if value is not None:
			if 'T' not in str(value):
				date_time = str(value) + 'T' + str(current_time)
				print('date_time: ', date_time)
				filtered_data[key] = date_time
			elif 'T' in str(value):
				filtered_data[key] = value

	serializer = DiscountSerializer(discount, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DiscountSerializer, responses=DiscountSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.DISCOUNT_DELETE.name])
def deleteDiscount(request, pk):
	try:
		discount = Discount.objects.get(pk=pk)
		discount.delete()
		return Response({'detail': f'Discount id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Discount id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

