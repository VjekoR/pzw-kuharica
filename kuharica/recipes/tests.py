from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Recipe, Category, Comment, Ingredient, RecipeIngredient

User = get_user_model()


class RecipeAppTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="u1", password="pass12345")
        self.user2 = User.objects.create_user(username="u2", password="pass12345")

        self.cat = Category.objects.create(name="Desserts")

        self.recipe = Recipe.objects.create(
            author=self.user1,
            title="Pancakes",
            description="desc",
            instructions="mix and cook",
            prep_time_minutes=10,
            difficulty="easy",
        )
        self.recipe.categories.add(self.cat)

    def test_recipe_list_view_ok(self):
        url = reverse("recipes:recipe_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Pancakes")

    def test_anonymous_cannot_create_recipe(self):
        url = reverse("recipes:recipe_create")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp.url)

    def test_author_can_edit_recipe(self):
        self.client.login(username="u1", password="pass12345")
        url = reverse("recipes:recipe_update", args=[self.recipe.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_other_user_cannot_edit_recipe(self):
        self.client.login(username="u2", password="pass12345")
        url = reverse("recipes:recipe_update", args=[self.recipe.pk])
        resp = self.client.get(url)
 
        self.assertEqual(resp.status_code, 403)

    def test_logged_user_can_comment(self):
        self.client.login(username="u2", password="pass12345")
        url = reverse("recipes:comment_create", args=[self.recipe.pk])
        resp = self.client.post(url, {"content": "Nice!"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Comment.objects.filter(recipe=self.recipe, content="Nice!").exists())

    def test_only_author_can_add_ingredient(self):
        add_url = reverse("recipes:ingredient_add", args=[self.recipe.pk])

        self.client.login(username="u2", password="pass12345")
        resp = self.client.post(add_url, {"name": "Salt", "quantity": "1", "unit": "tsp"})
        self.assertEqual(resp.status_code, 403)

        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(add_url, {"name": "Salt", "quantity": "1", "unit": "tsp"})
        self.assertEqual(resp.status_code, 302)

        ing = Ingredient.objects.get(name="Salt")
        self.assertTrue(RecipeIngredient.objects.filter(recipe=self.recipe, ingredient=ing).exists())