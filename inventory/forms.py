from django import forms
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement

class IngredientForm(forms.ModelForm):
  class Meta:
    model = Ingredient
    fields = "__all__"    #fields = ("name", "quantity", "unit", "unit_price")

class MenuItemForm(forms.ModelForm):
  class Meta:
    model = MenuItem
    fields = "__all__"    #fields = ("title", "price")

class PurchaseForm(forms.ModelForm):
  class Meta:
    model = Purchase
    fields = "__all__"    #fields = ("menu_item", "timestamp")

class RecipeRequirementForm(forms.ModelForm):
  class Meta:
    model = RecipeRequirement
    fields = "__all__"    #fields = ("menu_item", "ingredient", "quantity")