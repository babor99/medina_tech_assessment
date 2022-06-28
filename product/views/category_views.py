from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from product.models import Brand, Category, Product
from product.serializers import BrandSerializer, CategorySerializer, CategoryCustomSerializer, CategoryTreeSerializer, CategoryListSerializer, ProductListSerializer, ProductSerializer
from product.filters import CategoryFilter

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=CategorySerializer,
	responses=CategorySerializer
)
@api_view(['GET'])
def getAllCategory(request):
	categories = Category.objects.all()
	total_elements = categories.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	categories = pagination.paginate_data(categories)

	serializer = CategoryListSerializer(categories, many=True)

	response = {
		'categories': serializer.data,
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
	request=CategorySerializer,
	responses=CategorySerializer
)
@api_view(['GET'])
def getAllParentCategoryWithoutPagination(request):
	categories = Category.objects.filter(parent__isnull=True)

	serializer = CategoryListSerializer(categories, many=True)

	response = {
		'parent_categories': serializer.data,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=CategorySerializer,
	responses=CategorySerializer
)
@api_view(['GET'])
def getAllSubCategoryByCategoryIdWithoutPagination(request, pk):
	categories = Category.objects.filter(parent__id=pk)

	serializer = CategoryListSerializer(categories, many=True)

	response = {
		'sub_categories': serializer.data,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=CategorySerializer,
	responses=CategorySerializer
)
@api_view(['GET'])
def getAllSubSubCategoryByCategoryIdWithoutPagination(request, pk):
	categories = Category.objects.filter(parent__id=pk)

	serializer = CategoryListSerializer(categories, many=True)

	response = {
		'sub_sub_categories': serializer.data,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(

	request=CategorySerializer,
	responses=CategorySerializer
)
@api_view(['GET'])
def getAllCategoryWithoutPagination(request):
	categories = Category.objects.all()

	serializer = CategoryListSerializer(categories, many=True)

	return Response({'categories': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=CategoryListSerializer, responses=CategoryListSerializer)
@api_view(['GET'])
def getACategory(request, pk):
	try:
		category = Category.objects.get(pk=pk)
		serializer = CategorySerializer(category)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Category id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CategorySerializer, responses=CategorySerializer)
@api_view(['GET'])
def searchCategory(request):
	categories = CategoryFilter(request.GET, queryset=Category.objects.all())
	categories = categories.qs

	print('searched_products: ', categories)

	total_elements = categories.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	categories = pagination.paginate_data(categories)

	serializer = CategoryListSerializer(categories, many=True)

	response = {
		'categories': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(categories) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no categories matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CategorySerializer, responses=CategorySerializer)
@api_view(['POST'])
def createCategory(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	print('data: ', data)
	print('filtered_data: ', filtered_data)

	serializer = CategorySerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CategorySerializer, responses=CategorySerializer)
@api_view(['PUT'])
def updateCategory(request, pk):
	data = request.data
	print('category data: ', data)
	filtered_data = {}
	
	try:
		category = Category.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"Category id - {pk} doesn't exists"})

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	print('filtered_data: ', filtered_data)
		
	icon = filtered_data.get('icon', None)
	image = filtered_data.get('image', None)

	if icon is not None and type(icon) == str:
		popped_icon = filtered_data.pop('icon')
	if image is not None and type(image) == str:
		popped_image = filtered_data.pop('image')

	serializer = CategorySerializer(category, data=filtered_data)
	
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors)




@extend_schema(request=CategorySerializer, responses=CategorySerializer)
@api_view(['DELETE'])
def deleteCategory(request, pk):
	try:
		category = Category.objects.get(pk=pk)
		category.delete()
		return Response({'detail': f'Category id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Category id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)



