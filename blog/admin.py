from django.contrib import admin
from .models import Post, Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

# Register your models here.
admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)

