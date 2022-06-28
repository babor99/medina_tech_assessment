
from django.urls import path
from product.views import productimage_views as views


urlpatterns = [
	path('api/v1/productimage/all/', views.getAllProductImage),

	path('api/v1/productimage/all_productimage_by_product_id/<int:product_id>', views.getAllProductImageByProductId),

	path('api/v1/productimage/<int:pk>', views.getAProductImage),

	path('api/v1/productimage/search/', views.searchProductImage),

	path('api/v1/productimage/create/', views.createProductImage),

	path('api/v1/productimage/delete/<int:pk>', views.deleteProductImage),

	path('api/v1/productimage/update/<int:pk>', views.updateProductImage),

]