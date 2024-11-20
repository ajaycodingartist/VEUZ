from django.contrib import admin
from .models import Employee, EmployeeField

# Register your models here.


# Customizing the Employee model's admin interface
class EmployeeFieldInline(admin.TabularInline):
    model = EmployeeField
    extra = 1  # Display 1 empty row for new fields

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'position', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'position')
    list_filter = ('position', 'created_at')
    ordering = ('-created_at',)
    
    # Inline EmployeeField in the Employee form to manage fields directly from Employee form
    inlines = [EmployeeFieldInline]

    exclude = ('created_at', 'updated_at')

    # Optionally, you can define fieldsets to group the fields in the admin
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'position')
        }),

    )

# Register the Employee model with its custom admin interface
admin.site.register(Employee, EmployeeAdmin)

# Customizing the EmployeeField model's admin interface
class EmployeeFieldAdmin(admin.ModelAdmin):
    list_display = ('employee', 'field_name', 'field_value')
    search_fields = ('field_name', 'field_value')
    list_filter = ('employee',)
    ordering = ('employee',)

# Register the EmployeeField model with its custom admin interface
admin.site.register(EmployeeField, EmployeeFieldAdmin)
