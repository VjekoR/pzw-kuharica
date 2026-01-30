from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path("<int:pk>/", views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("create/", views.RecipeCreateView.as_view(), name="recipe_create"),
    path("<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="recipe_update"),
    path("<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipe_delete"),

    path("<int:pk>/comment/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),
    path("<int:pk>/ingredient/add/", views.AddIngredientToRecipeView.as_view(), name="ingredient_add"),
    path("register/", views.RegisterView.as_view(), name="register"),
]