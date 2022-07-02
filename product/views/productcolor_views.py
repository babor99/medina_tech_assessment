from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from product.models import Product, ProductColor
from product.serializers import ProductColorSerializer, ProductColorListSerializer
from product.filters import ProductColorFilter

from commons.pagination import Pagination
from commons.enums import ProductPermEnum



# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ProductColorSerializer,
	responses=ProductColorSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_COLOR_LIST.name])
def getAllProductColor(request):
	productcolors = ProductColor.objects.all()
	total_elements = productcolors.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	productcolors = pagination.paginate_data(productcolors)

	serializer = ProductColorListSerializer(productcolors, many=True)

	response = {
		'productcolors': serializer.data,
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
	request=ProductColorSerializer,
	responses=ProductColorSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_COLOR_LIST.name])
def getAllProductColorByProductId(request, product_id):
	try:
		product_obj = Product.objects.get(pk=product_id)
	except ObjectDoesNotExist:
		return Response(f"Product with id {product_id} doesn't exists.")

	productcolors = ProductColor.objects.filter(product=product_obj)

	serializer = ProductColorListSerializer(productcolors, many=True)

	return Response({'product_colors': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ProductColorSerializer, responses=ProductColorSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_COLOR_DETAILS.name])
def getAProductColor(request, pk):
	try:
		productcolor = ProductColor.objects.get(pk=pk)
		serializer = ProductColorListSerializer(productcolor)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductColor id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductColorSerializer, responses=ProductColorSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_COLOR_DETAILS.name])
def getAProductColorByProductId(request, product_id):

	try:
		productcolor = ProductColor.objects.get(product__id=product_id)
		print('productcolor: ', productcolor)
		serializer = ProductColorListSerializer(productcolor)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductColor for product {product_obj.name} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductColorSerializer, responses=ProductColorSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_COLOR_LIST.name])
def searchProductColor(request):
	product_colors = ProductColorFilter(request.GET, queryset=ProductColor.objects.all())
	product_colors = product_colors.qs

	print('searched_products: ', product_colors)

	total_elements = product_colors.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_colors = pagination.paginate_data(product_colors)

	serializer = ProductColorListSerializer(product_colors, many=True)

	response = {
		'product_colors': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(product_colors) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no product_colors matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductColorSerializer, responses=ProductColorSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_COLOR_CREATE.name])
def createProductColor(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = ProductColorSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductColorSerializer, responses=ProductColorSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_COLOR_UPDATE.name])
def updateProductColor(request,pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
	try:
		productcolor = ProductColor.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductColor id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
		
	serializer = ProductColorSerializer(productcolor, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductColorSerializer, responses=ProductColorSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.PRODUCT_COLOR_DELETE.name])
def deleteProductColor(request, pk):
	try:
		productcolor = ProductColor.objects.get(pk=pk)
		productcolor.delete()
		return Response({'detail': f'ProductColor id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductColor id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

