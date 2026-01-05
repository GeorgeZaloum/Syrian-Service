from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_request_list_create, name='service-request-list-create'),
    path('<int:request_id>/', views.service_request_detail, name='service-request-detail'),
    path('<int:request_id>/accept/', views.accept_service_request, name='service-request-accept'),
    path('<int:request_id>/reject/', views.reject_service_request, name='service-request-reject'),
]
