from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, Comment

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ["ingredient"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "prep_time_minutes", "difficulty", "created_at")
    list_filter = ("difficulty", "categories")
    search_fields = ("title", "description", "instructions", "author__username")
    date_hierarchy = "created_at"
    autocomplete_fields = ["author"]
    filter_horizontal = ("categories",)
    inlines = [RecipeIngredientInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("recipe", "author", "created_at")
    search_fields = ("content", "recipe__title", "author__username")
    date_hierarchy = "created_at"
