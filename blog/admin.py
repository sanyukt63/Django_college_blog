from django.contrib import admin
from .models import Post, Comment



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'slug', 'author', 'status', 'publish')
    list_filter = ('status', 'created', 'publish', 'author', 'tags')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status',)
    # filter_horizontal = ('tags',)  # Disabled: TaggableManager incompatible
    date_hierarchy = 'publish'



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']


    def approve_comments(self, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Mark selected comments as approved."

