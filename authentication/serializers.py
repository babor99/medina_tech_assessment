from django.contrib.auth import get_user_model
from django.db.models import fields
from django_currentuser.middleware import (get_current_authenticated_user, get_current_user)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import *

User = get_user_model()


# Serializers

class AdminUserMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'first_name', 'last_name', 'username', 'image']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}




class AdminUserListSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()
	
	class Meta:
		model = User
		exclude = ['password']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
	
	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by




		



class AdminUserListSerializerForGeneralUse(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()
	
	class Meta:
		model = User
		exclude = ['password', 'role', 'user_type', 'last_login']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}

	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by




class AdminUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'
		extra_kwargs = {
			'password': {
				'write_only': True,
				'required': False,
			},
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}

	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		modelObject.set_password(validated_data["password"])
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class PasswordChangeSerializer(serializers.Serializer):
	password = serializers.CharField(max_length=64)
	confirm_password = serializers.CharField(max_length=64)




class PermissionListSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()
	class Meta:
		model = Permission
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by




class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class RoleListSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()
	class Meta:
		model = Role
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by




class RoleMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = ['id', 'name']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		



class RoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class CountryListSerializer(serializers.ModelSerializer):
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()
	class Meta:
		model = Country
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		



class CountryMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Country
		fields = ['id', 'name']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		



class CountrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Country
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class CityListSerializer(serializers.ModelSerializer):
	country = CountryMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()
	class Meta:
		model = City
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		



class CityMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = City
		fields = ['id', 'name']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}




class CitySerializer(serializers.ModelSerializer):
	class Meta:
		model = City
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class VendorListSerializer(serializers.ModelSerializer):
	role = RoleMinimalListSerializer()
	city = CityMinimalListSerializer()
	country = CountryMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()
	class Meta:
		model = Vendor
		exclude = ['password', 'email_token', 'phone_otp']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		



class VendorMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendor
		fields = ['id', 'name']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}




class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendor
		fields = '__all__'

		extra_kwargs = {
			'password': {
				'write_only': True,
				'required': False,
			}
		}
	
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		modelObject.set_password(validated_data["password"])

		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class CustomerListSerializer(serializers.ModelSerializer):
	role = RoleMinimalListSerializer()
	city = CityMinimalListSerializer()
	country = CountryMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()
	class Meta:
		model = Customer
		exclude = ['password', 'email_token', 'phone_otp']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		



class CustomerMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ['id', 'name']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		



class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = '__all__'
		extra_kwargs = {
			'password': {
				'write_only': True,
				'required': False,
			},
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		modelObject.set_password(validated_data["password"])
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject

