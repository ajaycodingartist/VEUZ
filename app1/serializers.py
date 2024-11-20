from rest_framework import serializers
from .models import Employee, EmployeeField


class EmployeeFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeField
        fields = ['id', 'field_name', 'field_value']


class EmployeeSerializer(serializers.ModelSerializer):
    fields = EmployeeFieldSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'fields', 'created_at', 'updated_at']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        employee = Employee.objects.create(**validated_data)
        for field_data in fields_data:
            EmployeeField.objects.create(employee=employee, **field_data)
        return employee

    def update(self, instance, validated_data):

        fields_data = validated_data.pop('fields', [])
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.position = validated_data.get('position', instance.position)
        instance.save()

        for field_data in fields_data:
            field, created = EmployeeField.objects.update_or_create(
                employee=instance,
                field_name=field_data['field_name'],
                defaults={'field_value': field_data['field_value']}
            )
        return instance
