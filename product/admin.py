from django.contrib import admin
from product.models import *




# Register your models here.

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Brand._meta.fields]
	list_per_page = 16


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Category._meta.fields]
	list_per_page = 16


@admin.register(WeatherType)
class WeatherTypeAdmin(admin.ModelAdmin):
	list_display = [field.name for field in WeatherType._meta.fields]
	list_per_page = 16



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Product._meta.fields]
	list_per_page = 16


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Discount._meta.fields]
	list_per_page = 16


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Color._meta.fields]
	list_per_page = 16


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ProductColor._meta.fields]
	list_per_page = 16


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Size._meta.fields]
	list_per_page = 16


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ProductSize._meta.fields]
	list_per_page = 16


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ProductImage._meta.fields]
	list_per_page = 16


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Stock._meta.fields]
	list_per_page = 16






