from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    instructions = models.TextField()

    prep_time_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Preparation time in minutes",
    )

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
    )

    categories = models.ManyToManyField(
        Category,
        related_name="recipes",
        blank=True,
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("recipes:recipe_detail", args=[self.pk])

class RecipeIngredient(models.Model):
    """
    Through table between Recipe and Ingredient so we can store quantity + unit.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipes",
    )

    quantity = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Use 0 if not applicable",
        default=0,
    )

    unit = models.CharField(
        max_length=30,
        blank=True,
        help_text="e.g. g, ml, tbsp, tsp, pcs",
    )

    class Meta:
        unique_together = ("recipe", "ingredient")
        ordering = ["ingredient__name"]

    def __str__(self) -> str:
        q = f"{self.quantity:g}" if self.quantity is not None else ""
        u = self.unit.strip()
        qty_unit = f"{q} {u}".strip()
        return f"{self.recipe.title} -> {self.ingredient.name}" + (f" ({qty_unit})" if qty_unit else "")


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.recipe}"
