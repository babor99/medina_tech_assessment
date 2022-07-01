from authentication.models import *
from django_filters import rest_framework as filters



# Filters

class CityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = City
        fields = ['name', ]




class CountryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Country
        fields = ['name', ]




class PermissionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Permission
        fields = ['name', ]




class RoleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Role
        fields = ['name', ]




class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr='icontains')
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', 'email']




class VendorFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr='icontains')
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')

    class Meta:
        model = Vendor
        fields = ['username', 'email']




class CustomerFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr='icontains')
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['username', 'email']




