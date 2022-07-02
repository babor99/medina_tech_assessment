from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from product.models import WeatherType
from product.serializers import WeatherTypeSerializer, WeatherTypeListSerializer
from product.filters import WeatherTypeFilter

from commons.pagination import Pagination
from commons.enums import ProductPermEnum




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=WeatherTypeSerializer,
	responses=WeatherTypeSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.WEATHER_TYPE_LIST.name])
def getAllWeatherType(request):
	weather_types = WeatherType.objects.all()
	total_elements = weather_types.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	weather_types = pagination.paginate_data(weather_types)

	serializer = WeatherTypeListSerializer(weather_types, many=True)

	response = {
		'weather_types': serializer.data,
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
	request=WeatherTypeSerializer,
	responses=WeatherTypeSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.WEATHER_TYPE_LIST.name])
def getAllWeatherTypeWithoutPagination(request):
	weather_types = WeatherType.objects.all()

	serializer = WeatherTypeListSerializer(weather_types, many=True)

	return Response({'weather_types': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=WeatherTypeSerializer, responses=WeatherTypeSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.WEATHER_TYPE_DETAILS.name])
def getAWeatherType(request, pk):
	try:
		weather_type = WeatherType.objects.get(pk=pk)
		serializer = WeatherTypeSerializer(weather_type)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"WeatherType id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=WeatherTypeSerializer, responses=WeatherTypeSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.WEATHER_TYPE_LIST.name])
def searchWeatherType(request):
	weather_types = WeatherTypeFilter(request.GET, queryset=WeatherType.objects.all())
	weather_types = weather_types.qs

	print('searched_products: ', weather_types)

	total_elements = weather_types.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	weather_types = pagination.paginate_data(weather_types)

	serializer = WeatherTypeListSerializer(weather_types, many=True)

	response = {
		'weather_types': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(weather_types) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no weather_types matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=WeatherTypeSerializer, responses=WeatherTypeSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.WEATHER_TYPE_CREATE.name])
def createWeatherType(request):
	data = request.data
	itered_data = {}
	filtered_data = {}

	for key, value in data.items():
		itered_data[key] = value

	for key, value in itered_data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	print('data: ', data)
	print('itered_data: ', itered_data)
	print('filtered_data: ', filtered_data)

	serializer = WeatherTypeSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=WeatherTypeSerializer, responses=WeatherTypeSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.WEATHER_TYPE_UPDATE.name])
def updateWeatherType(request,pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	try:
		weather_type = WeatherType.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"WeatherType id - {pk} doesn't exists"})

	image = filtered_data.get('image', None)
	if type(image) == str and image is not None:
		poped_image = filtered_data.pop('image')

	serializer = WeatherTypeSerializer(weather_type, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=WeatherTypeSerializer, responses=WeatherTypeSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@has_permissions([ProductPermEnum.WEATHER_TYPE_DELETE.name])
def deleteWeatherType(request, pk):
	try:
		weather_type = WeatherType.objects.get(pk=pk)
		weather_type.delete()
		return Response({'detail': f'WeatherType id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"WeatherType id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
