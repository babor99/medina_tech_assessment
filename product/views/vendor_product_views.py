from itertools import product
from os import stat
from platform import release
from turtle import RawTurtle
from django.core.exceptions import ObjectDoesNotExist
from product.admin import StockAdmin

from rest_framework import status
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sequences import get_next_value

from drf_spectacular.utils import OpenApiParameter, extend_schema

from authentication.decorators import has_permissions

from product.models import Brand, Category, Discount, Product, Stock, WeatherType
from product.serializers import ProductSerializer, ProductListSerializer, StockSerializer
from product.filters import ProductFilter

from product.utils import decimalize_list

from commons.pagination import Pagination
from commons import constants
from commons.enums import ProductPermEnum




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ProductSerializer,
	responses=ProductSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([ProductPermEnum.PRODUCT_LIST.name])
def getAllProductOfVendor(request):
	user = request.user
	if user.user_type == 'vendor':
		products = Product.objects.filter(vendor=user)
		total_elements = products.count()

		page = request.query_params.get('page')
		size = request.query_params.get('size')

		# Pagination
		pagination = Pagination()
		pagination.page = page
		pagination.size = size
		products = pagination.paginate_data(products)

		serializer = ProductListSerializer(products, many=True)

		response = {
			'products': serializer.data,
			'page': pagination.page,
			'size': pagination.size,
			'total_pages': pagination.total_pages,
			'total_elements': total_elements,
		}
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"{user.first_name} is not a vendor account. Please login with vendor account."}, status=status.HTTP_403_FORBIDDEN)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_DETAILS.name])
def getAProductOfVendor(request, pk):
	user = request.user
	try:
		product = Product.objects.get(vendor=user, pk=pk)
		serializer = ProductListSerializer(product)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"You don't own this product to delete or Product id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_LIST.name])
def searchVendorProduct(request):
	searched_products = ProductFilter(request.GET, queryset=Product.objects.filter(vendor=request.user))
	searched_products = searched_products.qs

	print('searched_products: ', searched_products)

	total_elements = searched_products.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	searched_products = pagination.paginate_data(searched_products)

	serializer = ProductListSerializer(searched_products, many=True)

	response = {
		'products': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(searched_products) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no products matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_CREATE.name])
def createVendorProduct(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}
	stock_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	print('filtered_data: ', filtered_data)

	quantity = filtered_data.get('quantity', None)
	if quantity:
		stock_data['quantity'] = quantity
	else:
		stock_data['quantity'] = 1

	filtered_data['condition'] = 'NEW'

	serializer = ProductSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		stock_serializer = StockSerializer(data=stock_data)
		if stock_serializer.is_valid():
			stock_serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_UPDATE.name])
def updateVendorProduct(request,pk):
	data = request.data
	print('product data: ', data)
	filtered_data = {}

	try:
		product = Product.objects.get(vendor=request.user, pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"You don't own this product to delete or Product id - {pk} doesn't exists"})

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	thumbnail = filtered_data.get('thumbnail', None)

	if thumbnail and type(thumbnail) == str:
		popped_thumbnail = filtered_data.pop('thumbnail')

	print('filtered_data: ', filtered_data)

	serializer = ProductSerializer(product, data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_DELETE.name])
def deleteVendorProduct(request, pk):
	user = request.user
	try:
		product = Product.objects.get(vendor=user, pk=pk)
		product.delete()
		return Response({'detail': f'Product id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"You don't own this product to delete or Product id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
