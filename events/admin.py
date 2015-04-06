from django.contrib import admin
from events.models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['cat_id']}),
        (None,              {'fields': ['short_name']}),
    ]
    list_display = ('cat_id', 'short_name')
    list_filter = ['short_name']
    search_fields = ['short_name']

admin.site.register(Category, CategoryAdmin)

