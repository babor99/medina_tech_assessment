from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sequences import get_next_value

from drf_spectacular.utils import OpenApiParameter, extend_schema

from product.models import Brand, Category, Discount, Product, WeatherType
from product.serializers import DiscountListSerializer, ProductListSerializerWithDiscount, ProductSerializer, ProductListSerializer
from product.filters import ProductFilterByNameCat, ProductFilterByBrandRatingPrice, ProductImageFilter

from product.utils import decimalize_list

from commons.pagination import Pagination
from commons import constants
from itertools import chain
import requests



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
def getAllProductOfUserLocWeather(request):
	user_city = request.user.city
	if user_city:
		lat = user_city.lat
		lon = user_city.lon
		res = requests.get(str(constants.WEATHER_API_URL)+f'?lat={lat}&lon={lon}&appid={constants.WEATHER_API_KEY}')
		temp = 12
		print('res: ', res.data)
		weather_types = WeatherType.objects.filter(temp_high__gte=temp, temp_low__lte=temp)
		products = Product.objects.filter(product_type__in=weather_types)
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
		return Response({'detail': f""})



@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ProductSerializer,
	responses=ProductSerializer
)
@api_view(['GET'])
def getAllProduct(request):
	products = Product.objects.all()
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




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ProductSerializer,
	responses=ProductSerializer
)
@api_view(['GET'])
def getAllProductOfIndividualVendor(request):
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




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ProductSerializer,
	responses=ProductSerializer
)
@api_view(['GET'])
def getAllProductWithoutPagination(request):
	products = Product.objects.all()

	serializer = ProductListSerializer(products, many=True)

	return Response({'products': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
def getAProduct(request, pk):
	try:
		product = Product.objects.get(pk=pk)
		serializer = ProductListSerializer(product)
	
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Product id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
def getAProductOfIndividualVendor(request, pk):
	user = request.user
	if user.user_type == 'vendor':
		try:
			product = Product.objects.get(vendor=user, pk=pk)
			serializer = ProductListSerializer(product)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response({'detail': f"Product id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response({'detail': f"{user.first_name} is not a vendor account. Please login with vendor account."}, status=status.HTTP_403_FORBIDDEN)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
def getAllProductUsingCategory(request, category_id):
	category_obj = Category.objects.get(pk=int(category_id))
	products = Product.objects.filter(category=category_obj)

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




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
def getAllProductUsingCategoryNested(request, category_id):

	category_obj = Category.objects.filter(pk=category_id)
	first_childs = Category.objects.filter(parent__in=category_obj)
	second_childs = Category.objects.filter(parent__in=first_childs)
	print('category: ', category_obj)
	print('first_childs: ', first_childs)
	print('second_childs: ', second_childs)

	chained_categories = list(chain(category_obj, first_childs, second_childs))
	print('chained_categories: ', chained_categories)

	products = Product.objects.filter(category__in=chained_categories)

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




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
def getAllProductUsingBrand(request, brand_id):
	brand_obj = Brand.objects.get(pk=int(brand_id))
	products = Product.objects.filter(brand=brand_obj)

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




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
def searchProduct(request):

	searched_products = ProductFilterByNameCat(request.GET, queryset=Product.objects.all())
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
		return Response({'detail': f"There are no products matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['GET'])
def filterProduct(request):
	query_params_dict = dict(request.query_params)
	print('query_params_dict: ', query_params_dict)
	ratings = query_params_dict.get('rating', None)
	print('ratings: ', ratings)
	print('type(ratings): ', type(ratings))

	category_id = request.query_params.get('category')
	category_objs = Category.objects.filter(pk=category_id)

	first_childs = Category.objects.filter(parent__in=category_objs)
	second_childs = Category.objects.filter(parent__in=first_childs)
	print('category_id: ', category_id)
	print('category_objs: ', category_objs)
	print('first_childs: ', first_childs)
	print('second_childs: ', second_childs)

	chained_categories = list(chain(category_objs, first_childs, second_childs))
	print('chained_categories: ', chained_categories)


	if ratings is not None:
		extended_ratings = decimalize_list(ratings)
		print('extended_ratings: ', extended_ratings)
		products = Product.objects.filter(category__in=chained_categories, rating__in=extended_ratings)
	else:
		products = Product.objects.filter(category__in=chained_categories)

	print('products: ', products)

	filtered_products = ProductFilterByBrandRatingPrice(request.GET, queryset=products)
	filtered_products = filtered_products.qs

	print('request.query_params: ', request.query_params)
	print('request.GET: ', request.GET)
	print('filtered_products: ', filtered_products)

	total_elements = filtered_products.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	filtered_products = pagination.paginate_data(filtered_products)

	serializer = ProductListSerializer(filtered_products, many=True)

	response = {
		'products': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(filtered_products) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no products matching your filter"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['POST'])
def createProduct(request):
	data = request.data
	print('data: ', data)
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	print('filtered_data: ', filtered_data)

	filtered_data['condition'] = 'NEW'

	serializer = ProductSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['PUT'])
def updateProduct(request,pk):
	data = request.data
	print('product data: ', data)
	filtered_data = {}
	
	try:
		product = Product.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"Product id - {pk} doesn't exists"})

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
		return Response(serializer.errors)




@extend_schema(request=ProductSerializer, responses=ProductSerializer)
@api_view(['DELETE'])
def deleteProduct(request, pk):
	try:
		product = Product.objects.get(pk=pk)
		product.delete()
		return Response({'detail': f'Product id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Product id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
