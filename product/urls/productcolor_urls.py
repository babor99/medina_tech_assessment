
from django.urls import path
from product.views import productcolor_views as views


urlpatterns = [
	path('api/v1/productcolor/all/', views.getAllProductColor),

	path('api/v1/productcolor/get_all_by_product_id/<int:product_id>', views.getAllProductColorByProductId),

	path('api/v1/productcolor/<int:pk>', views.getAProductColor),

	path('api/v1/productcolor/get_by_product_id/<int:product_id>', views.getAProductColorByProductId),

	path('api/v1/productcolor/search/', views.searchProductColor),

	path('api/v1/productcolor/create/', views.createProductColor),

	path('api/v1/productcolor/delete/<int:pk>', views.deleteProductColor),

	path('api/v1/productcolor/update/<int:pk>', views.updateProductColor),

]