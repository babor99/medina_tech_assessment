from unicodedata import category
from rest_framework import serializers
from django.db import transaction

from django_currentuser.middleware import (get_current_authenticated_user, get_current_user)
from decimal import Decimal
from uuid import RESERVED_FUTURE

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from authentication.serializers import AdminUserMinimalListSerializer

from .models import *

from product.models import Category




class ProductMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
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
		



class BrandListSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()
	class Meta:
		model = Brand
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




class BrandMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brand
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
		



class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brand
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




class CategoryListSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()

	class Meta:
		model = Category
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




class CategoryMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
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
		



class CategoryTreeSerializer(serializers.ModelSerializer):
	children = RecursiveField(many=True)

	class Meta:
		model = Category
		fields = ['id', 'name', 'icon', 'image', 'parent', 'children']
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
		



class CategoryCustomSerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = ['id', 'name', 'image']
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
		



class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
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




class WeatherTypeListSerializer(serializers.ModelSerializer):
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()

	class Meta:
		model = WeatherType
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




class WeatherTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = WeatherType
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




class ProductListSerializer(serializers.ModelSerializer):
	brand = BrandMinimalListSerializer()
	category = CategoryMinimalListSerializer()
	vendor = AdminUserMinimalListSerializer()
	verified_by = AdminUserMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()

	class Meta:
		model = Product
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
		



class ProductListSerializerForInventory(serializers.ModelSerializer):
	category = CategoryMinimalListSerializer()
	class Meta:
		model = Product
		fields = ['id', 'name', 'unit_price', 'thumbnail', 'category']
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
		



class ProductCustomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'name', 'unit_price', 'short_desc', 'thumbnail', ]
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
		



class ProductMinimalListSerializer(serializers.ModelSerializer):
	category = serializers.SerializerMethodField()
	brand = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = ['id', 'name', 'unit_price', 'category', 'brand' ]
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
		
	def get_category(self, obj):
		return obj.category.name if obj.category else obj.category
	
	def get_brand(self, obj):
		return obj.brand.name if obj.brand else obj.brand
	



class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
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




class DiscountListSerializer(serializers.ModelSerializer):
	product = ProductMinimalListSerializer()
	discount_amount = serializers.SerializerMethodField()
	discounted_price = serializers.SerializerMethodField()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()

	class Meta:
		model = Discount
		fields = ['id', 'discount_percent', 'discount_amount', 'discounted_price', 'start_date', 'end_date', 'created_at', 'updated_at', 'created_by', 'updated_by', 'product',]
		depth = 1
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
		
	def get_discount_amount(self, obj):
		if obj.discount_percent:
			unit_price = Decimal(obj.product.unit_price)
			discount_percent = obj.discount_percent
			discount_amount = (unit_price * discount_percent) / 100
			return discount_amount
		else:
			return None

	def get_discounted_price(self, obj):
		if obj.discount_percent:
			unit_price = Decimal(obj.product.unit_price)
			discount_percent = obj.discount_percent
			discount_amount = (unit_price * discount_percent) / 100
			discounted_price = unit_price - discount_amount
			return discounted_price
		else:
			return None




class DiscountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Discount
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
	



class ProductTagListSerializer(serializers.ModelSerializer):
	product = ProductMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()
	class Meta:
		model = ProductTag
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
		



class ProductTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductTag
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




class ColorListSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField(read_only=True)
	updated_by = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Color
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




class ColorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Color
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




class ProductColorListSerializer(serializers.ModelSerializer):
	product = ProductMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()
	class Meta:
		model = ProductColor
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
		



class ProductColorSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductColor
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




class SizeListSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField(read_only=True)
	updated_by = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Size
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




class SizeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Size
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




class ProductSizeListSerializer(serializers.ModelSerializer):
	product = ProductMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()
	class Meta:
		model = ProductSize
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




class ProductSizeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductSize
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




class ProductImageListSerializer(serializers.ModelSerializer):
	product = ProductMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()
	class Meta:
		model = ProductImage
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




class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
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




class DiscountListSerializerForProduct(serializers.ModelSerializer):
	discount_amount = serializers.SerializerMethodField()
	discounted_price = serializers.SerializerMethodField()
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()

	class Meta:
		model = Discount
		fields = ['id', 'discount_percent', 'discount_amount', 'discounted_price', 'start_date', 'end_date', 'created_at', 'updated_at', 'created_by', 'updated_by']
		depth = 1
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
		
	def get_discount_amount(self, obj):
		if obj.discount_percent:
			unit_price = Decimal(obj.product.unit_price)
			discount_percent = obj.discount_percent
			discount_amount = (unit_price * discount_percent) / 100
			return discount_amount
		else:
			return None

	def get_discounted_price(self, obj):
		if obj.discount_percent:
			unit_price = Decimal(obj.product.unit_price)
			discount_percent = obj.discount_percent
			discount_amount = (unit_price * discount_percent) / 100
			discounted_price = unit_price - discount_amount
			return discounted_price
		else:
			return None

	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by




class ProductListSerializerWithDiscount(serializers.ModelSerializer):
	product_discount = DiscountListSerializerForProduct()
	brand = BrandMinimalListSerializer()
	category = CategoryMinimalListSerializer()
	vendor = AdminUserMinimalListSerializer()
	verified_by = AdminUserMinimalListSerializer()
	created_by = AdminUserMinimalListSerializer()
	updated_by = AdminUserMinimalListSerializer()

	class Meta:
		model = Product
		fields = ['product_discount', 'id', 'name', 'short_desc', 'full_desc', 'sku', 'gtin', 'barcode', 'attribute_set', 'brand', 'category', 'manufacturer', 'vendor', 'old_price', 'unit_price', 'condition', 'is_published', 'is_disabled', 'is_popular', 'is_featured', 'is_flash_deal', 'is_new_arrival', 'is_under_discount', 'is_available_for_preorder', 'allow_customer_review', 'mark_as_new', 'show_on_homepage', 'disable_wishlist_button', 'disable_buy_button', 'is_verified', 'verified_by', 'thumbnail', 'rating', 'num_reviews', 'display_order', 'expire_info', 'admin_comment', 'created_at', 'updated_at', 'created_by', 'updated_by' ]
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
		



