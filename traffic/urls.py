from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- Home & Public Map ---
    path('', views.home, name='home'),
    
    # --- Authentication System ---
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- Commuter Actions ---
    path('report-incident/', views.report_incident, name='report_incident'),

    # --- Authority/Police Dashboard ---
    path('authority/dashboard/', views.authority_dashboard, name='authority_dashboard'),

    # --- Engineer Dashboard & Road Management ---
    path('engineer/dashboard/', views.engineer_dashboard, name='engineer_dashboard'),
    path('engineer/create/', views.create_road_status, name='create_road_status'),
    path('engineer/edit/<int:pk>/', views.edit_road_status, name='edit_road_status'),

    # --- API Endpoints (For Leaflet Map) ---
    path('api/incidents/', views.api_incidents, name='api_incidents'),
    path('api/road-statuses/', views.api_road_statuses, name='api_road_statuses'),
]