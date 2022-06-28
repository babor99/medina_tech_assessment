
from django.urls import path
from product.views import discount_views as views


urlpatterns = [
	path('api/v1/discount/all/', views.getAllDiscount),

	path('api/v1/discount/without_pagination/all/', views.getAllDiscountWithoutPagination),

	path('api/v1/discount/get_a_discount_by_product_id/<int:product_id>', views.getADiscountByProductId),

	path('api/v1/discount/<int:pk>', views.getADiscount),
	
	path('api/v1/discount/search/', views.searchDiscount),

	path('api/v1/discount/create/', views.createDiscount),

	path('api/v1/discount/update/<int:pk>', views.updateDiscount),

	path('api/v1/discount/delete/<int:pk>', views.deleteDiscount),
]