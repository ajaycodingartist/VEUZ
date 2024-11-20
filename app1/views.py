from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Employee, EmployeeField
from .serializers import EmployeeSerializer, EmployeeFieldSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework import serializers

# Create your views here.


class HomePageView(TemplateView):
    template_name = "index.html"


# Employee ViewSet for CRUD Operations
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        fields_data = self.request.data.get('fields', [])
        employee = serializer.save()
        for field_data in fields_data:
            EmployeeField.objects.create(employee=employee, **field_data)
        return employee

    def perform_update(self, serializer):
        fields_data = self.request.data.get('fields', [])
        employee = serializer.save()
        for field_data in fields_data:
            EmployeeField.objects.update_or_create(
                employee=employee,
                field_name=field_data.get('field_name'),
                defaults={'field_value': field_data.get('field_value')}
            )
        return employee

# Employee Fields ViewSet
class EmployeeFieldViewSet(viewsets.ModelViewSet):
    queryset = EmployeeField.objects.all()
    serializer_class = EmployeeFieldSerializer
    permission_classes = [IsAuthenticated]

# JWT Authentication - Login and Token Views
class CustomTokenObtainPairView(TokenObtainPairView):

    pass

class TokenRefreshView(TokenRefreshView):

    pass

# Registration view for creating a new user (Admin, for example)
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if username and password and email:
            user = User.objects.create_user(username=username, password=password, email=email)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

# Profile management view for user profile
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

    if request.method == 'PUT':
        username = request.data.get('username')
        email = request.data.get('email')

        user = request.user
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()
        return Response({'message': 'Profile updated successfully'})

# Change Password View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        else:
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
