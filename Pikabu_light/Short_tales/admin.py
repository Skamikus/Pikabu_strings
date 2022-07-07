from django.contrib import admin
from .models import Posts, Category
# Register your models here.

class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'story_title', 'date_in', 'date_change', 'posted', 'category',)
    list_display_links = ('id', 'story_title',)
    search_fields = ('id', 'story_title', 'story_id',)
    list_editable = ('posted',)
    list_filter = ('posted', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)

admin.site.register(Posts, PostsAdmin)
admin.site.register(Category, CategoryAdmin)