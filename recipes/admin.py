from django.contrib import admin
from .models import Recipe, Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'tittle', 'created_at', 'is_published', 'author',
    list_display_links = 'tittle', 'created_at',
    search_fields = 'id', 'tittle', 'description', 'slug',
    list_filter = 'category', 'author', 'is_published',
    list_per_page = 15
    list_editable = 'is_published',
    ordering = 'id',
    prepopulated_fields = {"slug":('tittle', )}
admin.site.register(Category, CategoryAdmin)

