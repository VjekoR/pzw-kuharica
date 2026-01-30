from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from django.contrib.auth import login
from .models import Recipe, Comment, Ingredient, RecipeIngredient
from .forms import AddIngredientForm
from django.contrib.auth.views import LogoutView

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        qs = Recipe.objects.select_related("author").prefetch_related("categories")

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q)

        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(categories__id=category)

        return qs


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["ingredient_form"] = AddIngredientForm()
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = [
        "title",
        "description",
        "instructions",
        "prep_time_minutes",
        "difficulty",
        "categories",
    ]
    template_name = "recipes/recipe_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = [
        "title",
        "description",
        "instructions",
        "prep_time_minutes",
        "difficulty",
        "categories",
    ]
    template_name = "recipes/recipe_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = "recipes/recipe_confirm_delete.html"
    success_url = reverse_lazy("recipes:recipe_list")

    def test_func(self):
        return self.get_object().author == self.request.user
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.recipe = Recipe.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.recipe.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return self.object.recipe.get_absolute_url()

class AddIngredientToRecipeView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        return recipe.author == self.request.user

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        form = AddIngredientForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Invalid ingredient data.")
            return redirect(recipe.get_absolute_url())

        name = form.cleaned_data["name"].strip()
        quantity = form.cleaned_data.get("quantity") or 0
        unit = (form.cleaned_data.get("unit") or "").strip()

        ingredient, _ = Ingredient.objects.get_or_create(name=name)

        RecipeIngredient.objects.update_or_create(
            recipe=recipe,
            ingredient=ingredient,
            defaults={"quantity": quantity, "unit": unit},
        )

        messages.success(request, "Ingredient added/updated.")
        return redirect(recipe.get_absolute_url())

class HomeView(TemplateView):
    template_name = "home.html"

class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("recipes:recipe_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class LogoutGetView(LogoutView):
    http_method_names = ["get", "post", "options"]
