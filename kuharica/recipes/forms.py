from django import forms

class AddIngredientForm(forms.Form):
    name = forms.CharField(max_length=120, label="Ingredient")
    quantity = forms.DecimalField(required=False, min_value=0, decimal_places=2, max_digits=7)
    unit = forms.CharField(max_length=30, required=False)
