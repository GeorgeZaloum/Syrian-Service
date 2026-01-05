from django.urls import path
from .views import (
    ProblemReportCreateView,
    ProblemReportListView,
    ProblemReportDetailView
)

app_name = 'problems'

urlpatterns = [
    path('', ProblemReportListView.as_view(), name='problem-list'),
    path('create/', ProblemReportCreateView.as_view(), name='problem-create'),
    path('<int:pk>/', ProblemReportDetailView.as_view(), name='problem-detail'),
]
