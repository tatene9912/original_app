from django.contrib import admin
from .models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.resources import ModelResource

class UserResource(ModelResource):
    email = Field(attribute='email', column_name='email')
    nic_name = Field(attribute='nic_name', column_name='nic_name')
    name = Field(attribute='name', column_name='name')
    profile = Field(attribute='profile', column_name='profile')
    postal_code = Field(attribute='postal_code', column_name='postal_code')
    address = Field(attribute='address', column_name='address')
    phone_number = Field(attribute='phone_number', column_name='phone_number')
    is_superuser = Field(attribute='is_superuser', column_name='is_superuser')
    is_staff = Field(attribute='is_staff', column_name='is_staff')
    is_active = Field(attribute='is_active', column_name='is_active')

    class Meta:
        model = User
        skip_unchanged = True
        use_bulk = True
        exclude = ('some_abstract_field',) 

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'email', 'name', 'nic_name', 'profile', 'postal_code', 'address', 'phone_number', 'is_superuser', 'is_staff', 'is_active', 'created_at', 'updated_at')
    search_fields = ('email', 'name', )
    resource_class = UserResource
    list_filter = ['is_superuser', 'is_staff', 'is_active', ] 