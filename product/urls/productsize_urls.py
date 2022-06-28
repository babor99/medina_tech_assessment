
from django.urls import path
from product.views import productsize_views as views


urlpatterns = [
	path('api/v1/productsize/all/', views.getAllProductSize),

	path('api/v1/productsize/get_all_by_product_id/<int:product_id>', views.getAllProductSizeByProductId),

	path('api/v1/productsize/<int:pk>', views.getAProductSize),

	path('api/v1/productsize/get_by_product_id/<int:product_id>', views.getAProductSizeByProductId),
	
	path('api/v1/productsize/search/', views.searchProductSize),

	path('api/v1/productsize/create/', views.createProductSize),

	path('api/v1/productsize/delete/<int:pk>', views.deleteProductSize),

	path('api/v1/productsize/update/<int:pk>', views.updateProductSize),

]