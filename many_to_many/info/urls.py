from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_students_or_teachers/', views.get_students_or_teachers, name='get_students_or_teachers'),
    path('generate_certificate/', views.generate_certificate, name='generate_certificate'),
    path('verify_certificate/', views.verify_certificate, name='verify_certificate'),
]
