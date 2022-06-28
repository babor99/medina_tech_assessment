from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import OpenApiParameter, extend_schema

from product.models import Product, ProductTag
from product.serializers import ProductTagSerializer, ProductTagListSerializer
from product.filters import ProductTagFilter

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ProductTagSerializer,
	responses=ProductTagSerializer
)
@api_view(['GET'])
def getAllProductTag(request):
	product_tags = ProductTag.objects.all()
	total_elements = product_tags.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_tags = pagination.paginate_data(product_tags)

	serializer = ProductTagListSerializer(product_tags, many=True)

	response = {
		'product_tags': serializer.data,
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
	request=ProductTagSerializer,
	responses=ProductTagSerializer
)
@api_view(['GET'])
def getAllProductTagByProductId(request, product_id):
	try:
		product_obj = Product.objects.get(pk=product_id)
	except Product.DoesNotExist:
		return Response({'detail': f"Product id {product_id} doesn't exists."})

	product_tags = ProductTag.objects.filter(product=product_obj)

	serializer = ProductTagListSerializer(product_tags, many=True)

	return Response({'product_tags': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ProductTagSerializer, responses=ProductTagSerializer)
@api_view(['GET'])
def getAProductTag(request, pk):
	try:
		product_tag = ProductTag.objects.get(pk=pk)
		serializer = ProductTagListSerializer(product_tag)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductTag id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductTagSerializer, responses=ProductTagSerializer)
@api_view(['GET'])
def searchProductTag(request):
	product_tags = ProductTagFilter(request.GET, queryset=ProductTag.objects.all())
	product_tags = product_tags.qs

	print('searched_products: ', product_tags)

	total_elements = product_tags.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_tags = pagination.paginate_data(product_tags)

	serializer = ProductTagListSerializer(product_tags, many=True)

	response = {
		'product_tags': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(product_tags) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no product_tags matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductTagSerializer, responses=ProductTagSerializer)
@api_view(['POST'])
def createProductTag(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = ProductTagSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductTagSerializer, responses=ProductTagSerializer)
@api_view(['PUT'])
def updateProductTag(request,pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
	try:
		product_tag = ProductTag.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductTag id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
		
	serializer = ProductTagSerializer(product_tag, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductTagSerializer, responses=ProductTagSerializer)
@api_view(['DELETE'])
def deleteProductTag(request, pk):
	try:
		product_tag = ProductTag.objects.get(pk=pk)
		product_tag.delete()
		return Response({'detail': f'ProductTag id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductTag id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
