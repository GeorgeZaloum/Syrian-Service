from django.urls import path
from . import views

urlpatterns = [
    # Service CRUD endpoints
    path('', views.service_list_create, name='service-list-create'),
    path('<int:service_id>/', views.service_detail, name='service-detail'),
    path('my-services/', views.my_services, name='my-services'),
]
