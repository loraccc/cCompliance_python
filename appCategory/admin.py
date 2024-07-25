from django.contrib import admin
from appCategory.models import Category
from appSection.models import Section 
class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('sections',)
    list_display = ('name', 'description', 'get_section_names')
    search_fields = ('name', 'description')

    def get_section_names(self, obj):
        return ", ".join([section.name for section in obj.sections.all()])
    get_section_names.short_description = 'Section Names'

admin.site.register(Category, CategoryAdmin)