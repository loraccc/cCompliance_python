from django.contrib import admin
from appCategory.models import Category,Feature,CustomUser,Role
from appSection.models import Section 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('sections',)
    list_display = ('name', 'description', 'get_section_names')
    search_fields = ('name', 'description')

    def get_section_names(self, obj):
        return ", ".join([section.name for section in obj.sections.all()])
    get_section_names.short_description = 'Section Names'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Feature)
admin.site.register(Role)
# admin.site.register(CustomUser)



class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filter_horizontal = ['roles', 'groups', 'user_permissions']

admin.site.register(CustomUser, CustomUserAdmin)