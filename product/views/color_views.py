from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from product.models import Brand, Color
from product.serializers import ColorSerializer, ColorListSerializer
from product.filters import ColorFilter

from commons.pagination import Pagination
from commons.enums import ProductPermEnum




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ColorSerializer,
	responses=ColorSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.COLOR_LIST.name])
def getAllColor(request):
	colors = Color.objects.all()
	total_elements = colors.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	colors = pagination.paginate_data(colors)

	serializer = ColorListSerializer(colors, many=True)

	response = {
		'colors': serializer.data,
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
	request=ColorSerializer,
	responses=ColorSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.COLOR_LIST.name])
def getAllColorWithoutPagination(request):
	colors = Color.objects.all()

	serializer = ColorListSerializer(colors, many=True)

	return Response({'colors': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ColorSerializer, responses=ColorSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.COLOR_DETAILS.name])
def getAColor(request, pk):
	try:
		color = Color.objects.get(pk=pk)
		serializer = ColorSerializer(color)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Color id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ColorSerializer, responses=ColorSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.COLOR_LIST.name])
def searchColor(request):
	colors = ColorFilter(request.GET, queryset=Color.objects.all())
	colors = colors.qs

	print('searched_products: ', colors)

	total_elements = colors.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	colors = pagination.paginate_data(colors)

	serializer = ColorListSerializer(colors, many=True)

	response = {
		'colors': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(colors) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no colors matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ColorSerializer, responses=ColorSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.COLOR_CREATE.name])
def createColor(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = ColorSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ColorSerializer, responses=ColorSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.COLOR_UPDATE.name])
def updateColor(request,pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
	try:
		color = Color.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"Brand id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
		
	serializer = ColorSerializer(color, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ColorSerializer, responses=ColorSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.COLOR_DELETE.name])
def deleteColor(request, pk):
	try:
		color = Color.objects.get(pk=pk)
		color.delete()
		return Response({'detail': f'Color id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Color id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
