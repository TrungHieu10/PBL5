from django.urls import path
from . import views

urlpatterns = [
    path('sensor-data/', views.sensor_data, name='sensor_data'),
    path('sensor-data/get/', views.get_sensor_data, name='get_sensor_data'),
    path('', views.sensor_data_view, name='sensor_data_view'),  # Trang chính
]