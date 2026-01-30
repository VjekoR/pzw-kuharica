from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recipes.models import Category, Ingredient, Recipe, RecipeIngredient, Comment
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username="demo")
        user.set_password("demo12345")
        user.save()

        categories = ["Desserts", "Pasta", "Meat", "Salads"]
        category_objs = [Category.objects.get_or_create(name=c)[0] for c in categories]

        ingredients = ["Salt", "Sugar", "Flour", "Eggs", "Milk", "Butter"]
        ingredient_objs = [Ingredient.objects.get_or_create(name=i)[0] for i in ingredients]

        for i in range(5):
            recipe = Recipe.objects.create(
                author=user,
                title=f"Recipe {i+1}",
                description="Sample description",
                instructions="Sample instructions",
                prep_time_minutes=random.randint(5, 60),
                difficulty=random.choice(["easy", "medium", "hard"]),
            )
            recipe.categories.set(random.sample(category_objs, k=2))

            for ing in random.sample(ingredient_objs, k=3):
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ing,
                    quantity=random.randint(1, 5),
                    unit="pcs",
                )

            Comment.objects.create(
                recipe=recipe,
                author=user,
                content="Great recipe!",
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))