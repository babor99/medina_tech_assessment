from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from product.models import Product, ProductImage, Brand, Color
from product.serializers import ProductImageSerializer, ProductImageListSerializer
from product.filters import ProductImageFilter

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ProductImageSerializer,
	responses=ProductImageSerializer
)
@api_view(['GET'])
def getAllProductImage(request):
	product_images = ProductImage.objects.all()
	total_elements = product_images.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_images = pagination.paginate_data(product_images)

	serializer = ProductImageListSerializer(product_images, many=True)

	response = {
		'product_images': serializer.data,
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
	request=ProductImageSerializer,
	responses=ProductImageSerializer
)
@api_view(['GET'])
def getAllProductImageByProductId(request, product_id):
	try:
		product_obj = Product.objects.get(pk=int(product_id))
	except ObjectDoesNotExist:
		return Response(f"Product with id {product_id} doesn't exists.")
		
	product_images = ProductImage.objects.filter(product=product_obj)
	total_elements = product_images.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_images = pagination.paginate_data(product_images)

	serializer = ProductImageListSerializer(product_images, many=True)

	response = {
		'product_images': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(request=ProductImageSerializer, responses=ProductImageSerializer)
@api_view(['GET'])
def getAProductImage(request, pk):
	try:
		product_images = ProductImage.objects.get(pk=pk)
		serializer = ProductImageListSerializer(product_images)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Product Image id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductImageSerializer, responses=ProductImageSerializer)
@api_view(['GET'])
def searchProductImage(request):
	product_images = ProductImageFilter(request.GET, queryset=ProductImage.objects.all())
	product_images = product_images.qs

	print('searched_products: ', product_images)

	total_elements = product_images.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_images = pagination.paginate_data(product_images)

	serializer = ProductImageListSerializer(product_images, many=True)

	response = {
		'product_images': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(product_images) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no product_images matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductImageSerializer, responses=ProductImageSerializer)
@api_view(['POST'])
def createProductImage(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = ProductImageSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductImageSerializer, responses=ProductImageSerializer)
@api_view(['PUT'])
def updateProductImage(request, pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
	try:
		product_obj = Product.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"Product Image id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

	serializer = ProductImageSerializer(product_obj, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductImageSerializer, responses=ProductImageSerializer)
@api_view(['DELETE'])
def deleteProductImage(request, pk):
	try:
		product_image = ProductImage.objects.get(pk=pk)
		product_image.delete()
		return Response({'detail': f'Product Image id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Product Image id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
