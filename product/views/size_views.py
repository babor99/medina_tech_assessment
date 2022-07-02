from itertools import product
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from product.models import Size
from product.serializers import SizeSerializer, SizeListSerializer
from product.filters import SizeFilter

from commons.pagination import Pagination
from commons.enums import ProductPermEnum



# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=SizeSerializer,
	responses=SizeSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.SIZE_LIST.name])
def getAllSize(request):
	_sizes = Size.objects.all()
	total_elements = _sizes.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	_sizes = pagination.paginate_data(_sizes)

	serializer = SizeSerializer(_sizes, many=True)

	response = {
		'_sizes': serializer.data,
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
	request=SizeSerializer,
	responses=SizeSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.SIZE_LIST.name])
def getAllSizeWithoutPagination(request):
	sizes = Size.objects.all()

	serializer = SizeSerializer(sizes, many=True)

	return Response({'sizes': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=SizeSerializer, responses=SizeSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.SIZE_LIST.name])
def searchSize(request):
	sizes = SizeFilter(request.GET, queryset=Size.objects.all())
	sizes = sizes.qs

	print('searched_products: ', sizes)

	total_elements = sizes.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	sizes = pagination.paginate_data(sizes)

	serializer = SizeListSerializer(sizes, many=True)

	response = {
		'sizes': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(sizes) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no sizes matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=SizeSerializer, responses=SizeSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.SIZE_DETAILS.name])
def getASize(request, pk):
	try:
		_size = Size.objects.get(pk=pk)
		serializer = SizeSerializer(_size)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Size id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=SizeSerializer, responses=SizeSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.SIZE_CREATE.name])
def createSize(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = SizeSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=SizeSerializer, responses=SizeSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.SIZE_UPDATE.name])
def updateSize(request, pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
	try:
		_size = Size.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"Size id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
		
	serializer = SizeSerializer(_size, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=SizeSerializer, responses=SizeSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.SIZE_DELETE.name])
def deleteSize(request, pk):
	try:
		_size = Size.objects.get(pk=pk)
		_size.delete()
		return Response({'detail': f'Size id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Size id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

