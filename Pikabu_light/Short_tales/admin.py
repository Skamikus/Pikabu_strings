from django.contrib import admin
from .models import Posts
# Register your models here.

class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'story_title', 'date_in', 'date_change', 'posted',)
    list_display_links = ('id', 'story_title',)
    search_fields = ('id', 'story_title', 'story_id',)
    list_editable = ('posted',)
    list_filter = ('posted',)

admin.site.register(Posts, PostsAdmin)