from django.contrib import admin
from django.urls import path
from . import views

app_name='FAS'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('fas_home/', views.fas_home, name="fas_home"),
    path('fas_home/create_emp/', views.create_emp, name="create_emp"),
    path('fas_home/start_stop/', views.start_stop_sys, name="start_stop_sys"),
    path('fas_home/create_emp/cap_res/', views.cap_res, name="capture_result"),
    path('records/', views.records, name="records")
]
