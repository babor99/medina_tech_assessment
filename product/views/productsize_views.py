import re
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from product.models import Product, ProductSize
from product.serializers import ProductSizeSerializer, ProductSizeListSerializer
from product.filters import ProductSizeFilter

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ProductSizeSerializer,
	responses=ProductSizeSerializer
)
@api_view(['GET'])
def getAllProductSize(request):
	_productsizes = ProductSize.objects.all()
	total_elements = _productsizes.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	_productsizes = pagination.paginate_data(_productsizes)

	serializer = ProductSizeListSerializer(_productsizes, many=True)

	response = {
		'_productsizes': serializer.data,
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
	request=ProductSizeSerializer,
	responses=ProductSizeSerializer
)
@api_view(['GET'])
def getAllProductSizeByProductId(request, product_id):
	try:
		product_obj = Product.objects.get(pk=product_id)
	except Product.DoesNotExist:
		return Response({'detail': f"Product id {product_id} doesn't exists."})

	productsizes = ProductSize.objects.filter(product=product_obj)

	serializer = ProductSizeListSerializer(productsizes, many=True)

	return Response({'product_sizes': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ProductSizeSerializer, responses=ProductSizeSerializer)
@api_view(['GET'])
def getAProductSize(request, pk):
	try:
		_productsize = ProductSize.objects.get(pk=pk)
		serializer = ProductSizeListSerializer(_productsize)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductSize id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSizeSerializer, responses=ProductSizeSerializer)
@api_view(['GET'])
def getAProductSizeByProductId(request, product_id):
	try:
		product_obj = Product.objects.get(pk=int(product_id))
	except ObjectDoesNotExist:
		return Response({'detail': f"Product id - {product_id} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

	try:
		productsize = ProductSize.objects.get(product=product_obj)
		serializer = ProductSizeListSerializer(productsize)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductSize for product - {product_obj.name} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSizeSerializer, responses=ProductSizeSerializer)
@api_view(['GET'])
def searchProductSize(request):
	product_sizes = ProductSizeFilter(request.GET, queryset=ProductSize.objects.all())
	product_sizes = product_sizes.qs

	print('searched_products: ', product_sizes)

	total_elements = product_sizes.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_sizes = pagination.paginate_data(product_sizes)

	serializer = ProductSizeListSerializer(product_sizes, many=True)

	response = {
		'product_sizes': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(product_sizes) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no product_sizes matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSizeSerializer, responses=ProductSizeSerializer)
@api_view(['POST'])
def createProductSize(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = ProductSizeSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSizeSerializer, responses=ProductSizeSerializer)
@api_view(['PUT'])
def updateProductSize(request,pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
	try:
		_productsize = ProductSize.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductSize id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
		
	serializer = ProductSizeSerializer(_productsize, data=filtered_data)
	
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSizeSerializer, responses=ProductSizeSerializer)
@api_view(['DELETE'])
def deleteProductSize(request, pk):
	try:
		_productsize = ProductSize.objects.get(pk=pk)
		_productsize.delete()
		return Response({'detail': f'ProductSize id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductSize id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
