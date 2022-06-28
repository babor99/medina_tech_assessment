
from django.urls import path
from product.views import producttag_views as views


urlpatterns = [
	path('api/v1/producttag/all/', views.getAllProductTag),

	path('api/v1/producttag/get_all_by_product_id/<int:product_id>', views.getAllProductTagByProductId),

	path('api/v1/producttag/<int:pk>', views.getAProductTag),

	path('api/v1/producttag/search/', views.searchProductTag),

	path('api/v1/producttag/create/', views.createProductTag),

	path('api/v1/producttag/delete/<int:pk>', views.deleteProductTag),

	path('api/v1/producttag/update/<int:pk>', views.updateProductTag),

]