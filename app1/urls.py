from django.urls import path, include
from app1.views import HomePageView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeeFieldViewSet, CustomTokenObtainPairView, TokenRefreshView, register, profile, change_password

# Set up the router for Employee and EmployeeField ViewSets
router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')
router.register('fields', EmployeeFieldViewSet, basename='field')

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('api/', include(router.urls)),

    path('register/', register, name='register'),  # User registration
    path('profile/', profile, name='profile'),  # User profile
    path('change-password/', change_password, name='change_password'),


    
]