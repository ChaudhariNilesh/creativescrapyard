from django.urls import path
from .views import *
app_name = "Reports"
from model_report import report
report.autodiscover()
urlpatterns = [
  path('generate-reports/', reports, name='pivot_table'),
]