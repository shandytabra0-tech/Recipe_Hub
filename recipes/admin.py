from django.contrib import admin
from .models import Category, Recipe, Comment, Rating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'description': ('name',)}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'average_rating', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'average_rating']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'author', 'image')
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'instructions', 'prep_time', 'cook_time', 'servings')
        }),
        ('Status & Ratings', {
            'fields': ('status', 'average_rating', 'created_at', 'updated_at')
        }),
    )
    actions = ['approve_recipes', 'reject_recipes']

    def approve_recipes(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} recipe(s) approved.")
    approve_recipes.short_description = "Approve selected recipes"

    def reject_recipes(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} recipe(s) rejected.")
    reject_recipes.short_description = "Reject selected recipes"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['content', 'recipe__title', 'author__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['recipe__title', 'user__username']
    readonly_fields = ['created_at', 'updated_at']

