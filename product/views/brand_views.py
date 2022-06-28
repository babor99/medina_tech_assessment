from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from product.models import Brand
from product.serializers import BrandSerializer, BrandListSerializer
from product.filters import BrandFilter

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=BrandSerializer,
	responses=BrandSerializer
)
@api_view(['GET'])
def getAllBrand(request):
	brands = Brand.objects.all()
	total_elements = brands.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	brands = pagination.paginate_data(brands)

	serializer = BrandListSerializer(brands, many=True)

	response = {
		'brands': serializer.data,
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
	request=BrandSerializer,
	responses=BrandSerializer
)
@api_view(['GET'])
def getAllBrandWithoutPagination(request):
	brands = Brand.objects.all()

	serializer = BrandListSerializer(brands, many=True)

	return Response({'brands': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=BrandSerializer, responses=BrandSerializer)
@api_view(['GET'])
def getABrand(request, pk):
	try:
		brand = Brand.objects.get(pk=pk)
		serializer = BrandSerializer(brand)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Brand id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=BrandSerializer, responses=BrandSerializer)
@api_view(['GET'])
def getAllFeaturedBrand(request):
	brands = Brand.objects.filter(is_featured_brand=True)
	total_elements = brands.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	brands = pagination.paginate_data(brands)

	serializer = BrandListSerializer(brands, many=True)

	response = {
		'brands': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(brands) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no featured brands."}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=BrandSerializer, responses=BrandSerializer)
@api_view(['GET'])
def searchBrand(request):
	brands = BrandFilter(request.GET, queryset=Brand.objects.all())
	brands = brands.qs

	print('searched_products: ', brands)

	total_elements = brands.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	brands = pagination.paginate_data(brands)

	serializer = BrandListSerializer(brands, many=True)

	response = {
		'brands': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(brands) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no brands matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=BrandSerializer, responses=BrandSerializer)
@api_view(['POST'])
def createBrand(request):
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

	serializer = BrandSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors)




@extend_schema(request=BrandSerializer, responses=BrandSerializer)
@api_view(['PUT'])
def updateBrand(request,pk):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	try:
		brand = Brand.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"Brand id - {pk} doesn't exists"})

	image = filtered_data.get('image', None)
	if type(image) == str and image is not None:
		poped_image = filtered_data.pop('image')

	serializer = BrandSerializer(brand, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors)




@extend_schema(request=BrandSerializer, responses=BrandSerializer)
@api_view(['DELETE'])
def deleteBrand(request, pk):
	try:
		brand = Brand.objects.get(pk=pk)
		brand.delete()
		return Response({'detail': f'Brand id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Brand id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
