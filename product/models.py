from pyexpat import model
from django.db.models.lookups import BuiltinLookup
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.fields.related import ForeignKey

from authentication.models import Vendor, Customer


# Create your models here.

class Brand(models.Model):
	name = models.CharField(max_length=255)
	image = models.ImageField(upload_to='brand/', null=True, blank=True)

	is_featured_brand = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		ordering = ('-id', )


	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.title()
		super().save(*args, **kwargs)




class Category(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	icon = models.FileField(upload_to="category/", blank=True, null=True)
	image = models.ImageField(upload_to="category/", blank=True, null=True)

	parent = ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

	is_active = models.BooleanField(default=True)

	is_top_category = models.BooleanField(default=False)
	show_on_homepage = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	
	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-id',]
		verbose_name_plural = 'Categories'
	
	def save(self, *args, **kwargs):
		self.name = self.name.title()
		super().save(*args, **kwargs)




class WeatherType(models.Model):
	name = models.CharField(max_length=255)
	temp_low = models.DecimalField(max_digits=255, decimal_places=2, null=True, blank=True)
	temp_high = models.DecimalField(max_digits=255, decimal_places=2, null=True, blank=True)
	description = models.TextField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	
	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'WeatherTypes'
		ordering = ['-id',]
	
	def save(self, *args, **kwargs):
		self.name = self.name.replace(' ', '_').lower()
		super().save(*args, **kwargs)




class Product(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True)
	short_desc = models.TextField(blank=True, null=True)
	full_desc = models.TextField(blank=True, null=True)
	condition = models.CharField(max_length=255, null=True, blank=True)

	brand = models.ForeignKey(Brand, on_delete= models.SET_NULL, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	vendor = models.ForeignKey(Vendor, on_delete= models.SET_NULL, null=True, blank=True)
	product_type = models.ForeignKey(WeatherType, on_delete=models.SET_NULL, null=True, blank=True)

	old_price = models.DecimalField(default=0, max_digits=20, decimal_places=2, null=True, blank=True)
	unit_price = models.DecimalField(default=0, max_digits=20, decimal_places=2)

	is_popular = models.BooleanField(default=False)
	is_new_arrival = models.BooleanField(default=False)
	is_under_discount = models.BooleanField(default=False)
	is_verified = models.BooleanField(default=False)

	thumbnail = models.ImageField(upload_to="product/", null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.title()
		super().save(*args, **kwargs)




class Discount(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_discount', null=True, blank=True)

	discount_percent = models.IntegerField(default=0, null=True, blank=True)

	start_date = models.DateTimeField(null=True, blank=True)
	end_date = models.DateTimeField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		ordering = ('-id', )

	def __str__(self):
		return str(self.product)




class Color(models.Model):
	name = models.CharField(max_length=255)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		ordering = ('-id', )

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super().save(*args, **kwargs)




class ProductColor(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_color', null=True, blank=True)
	color = models.ManyToManyField(Color, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		verbose_name_plural = 'ProductColors'
		ordering = ('-id',)

	def __str__(self):
		return str(self.id)




class Size(models.Model):
	name = models.CharField(max_length=255)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super().save(*args, **kwargs)




class ProductSize(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_size', null=True, blank=True)
	size = models.ManyToManyField(Size, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		verbose_name_plural = 'ProductSizes'
		ordering = ('id',)

	def __str__(self):
		return str(self.id)




class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete= models.CASCADE, null=True, blank=True)
	image = models.ImageField(upload_to="productImage/", null=True, blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		verbose_name_plural = 'ProductImages'
		ordering = ('-id', )




