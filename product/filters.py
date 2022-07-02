from unicodedata import category
from django_filters import rest_framework as filters

from product.models import *




# custom filter
class AllValuesMultipleInFilter(filters.AllValuesMultipleFilter, filters.NumberFilter):
    pass




class BrandFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Brand
        fields = ['name',]




class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name',]




class ColorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Color
        fields = ['name',]




class WeatherTypeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = WeatherType
        fields = ['name', ]




class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    brand = filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    weather_type = filters.CharFilter(field_name='product_type__name', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='unit_price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'weather_type', 'min_price', 'max_price' ]




class ProductFilterByBrandRatingPrice(filters.FilterSet):
    brand = filters.AllValuesMultipleFilter(field_name='brand__id', lookup_expr='exact')
    min_price = filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='unit_price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['brand', 'min_price', 'max_price',]




class ProductReportFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    barcode = filters.CharFilter(field_name='barcode', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'category', 'barcode',]




class DiscountFilter(filters.FilterSet):
    product_name = filters.CharFilter(field_name="product__name", lookup_expr='icontains')

    class Meta:
        model = Discount
        fields = ['product_name',]




class ProductColorFilter(filters.FilterSet):
    product_name = filters.CharFilter(field_name="product__name", lookup_expr='icontains')

    class Meta:
        model = ProductColor
        fields = ['product_name',]




class ProductImageFilter(filters.FilterSet):
    product_name = filters.CharFilter(field_name="product__name", lookup_expr='icontains')

    class Meta:
        model = ProductImage
        fields = ['product_name',]




class ProductSizeFilter(filters.FilterSet):
    product_name = filters.CharFilter(field_name="product__name", lookup_expr='icontains')

    class Meta:
        model = ProductSize
        fields = ['product_name',]




class SizeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Size
        fields = ['name',]

