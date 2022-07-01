
from django.urls import path
from product.views import weather_type_views as views


urlpatterns = [

	path('api/v1/weather_type/all/', views.getAllWeatherType), #pagination done

	path('api/v1/weather_type/without_pagination/all/', views.getAllWeatherTypeWithoutPagination),

	path('api/v1/weather_type/<int:pk>', views.getAWeatherType),

	path('api/v1/weather_type/search/', views.searchWeatherType), #pagination done

	path('api/v1/weather_type/create/', views.createWeatherType),

	path('api/v1/weather_type/update/<int:pk>', views.updateWeatherType),

	path('api/v1/weather_type/delete/<int:pk>', views.deleteWeatherType),

]