from django.db import models

# Create your models here.
class Employee(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class EmployeeField(models.Model):

    employee = models.ForeignKey(Employee, related_name='fields', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    field_value = models.TextField()

    def __str__(self):
        return f"{self.field_name} for {self.employee.name}"