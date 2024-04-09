from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from inventory.models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum, F

# Create your views here.
class UserLogin(LoginView):
  success_url = reverse_lazy("profile")
  template_name = "registration/login.html"

class SignUp(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  template_name = "registration/signup.html"

def logout_view(request):
  logout(request)
  return redirect("login")

@login_required
def home(request):
  context = {"name": request.user.username}
  return render(request, "inventory/index.html", context) #inventory/home.html
  
def UserProfile(request):
  context = {"username": request.user.username}
  return render(request, "registration/profile.html", context)
  
def UserResetPassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')

            return redirect("/login")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/reset_password.html', {
        'form': form
    })
  
class IngredientList(LoginRequiredMixin, ListView):
  ingredients = Ingredient.objects.all()
  context = {"ingredients": ingredients}
  model = Ingredient
  template_name = "inventory/ingredient_list.html"

class IngredientCreate(LoginRequiredMixin, CreateView):
  model = Ingredient
  template_name = "inventory/ingredient_create_form.html"
  form_class = IngredientForm
  success_url = "ingredient/list"

class IngredientDetail(LoginRequiredMixin, DetailView):
  model = Ingredient
  template_name = "inventory/ingredient_details.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['object'] = self.object
    ingredient = Ingredient.objects.get(id=context['object'].pk)
    recipe_requirements_list = []
    for item in context['object'].reciperequirement_set.all():
      recipe_requirements_list.append(item)
    context = {
      'ingredient':ingredient,
      'recipe_requirements_list': recipe_requirements_list
    }
    return context

class IngredientUpdate(LoginRequiredMixin, UpdateView):
  model = Ingredient
  template_name = "inventory/ingredient_update_form.html"
  form_class = IngredientForm
  #success_url = "menuitem/list"

class IngredientDelete(LoginRequiredMixin, DeleteView):
  model = Ingredient
  template_name = "inventory/ingredient_delete_form.html"
  #success_url = "menuitem/list"

class MenuItemList(LoginRequiredMixin, ListView):
  model = MenuItem
  template_name = "inventory/menuitem_list.html"

class MenuItemCreate(LoginRequiredMixin, CreateView):
  model = MenuItem
  template_name = "inventory/menuitem_create.html"
  form_class = MenuItemForm
  success_url: "menuitem/list"

class MenuItemDetail(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = "inventory/menuitem_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        recipe_requirements = RecipeRequirement.objects.filter(menu_item=self.object)
        ingredients = []
        for item in recipe_requirements:
            ingredient_with_quantity = (item.ingredient, item.quantity)
            ingredients.append(ingredient_with_quantity)
        context['ingredients'] = ingredients
        return context

class MenuItemUpdate(LoginRequiredMixin, UpdateView):
  model = MenuItem
  template_name = "inventory/menuitem_update_form.html"
  form_class = MenuItemForm
  success_url: "menuitem/list"

class MenuItemDelete(LoginRequiredMixin, DeleteView):
  model = MenuItem
  template_name = "inventory/menuitem_delete_form.html"
  success_url = "menuitem/list"

class RecipeRequirementCreate(LoginRequiredMixin, CreateView):
  model = RecipeRequirement
  template_name: "inventory/reciperequirement_form.html"
  form_class = RecipeRequirementForm
  success_url: "menuitem/list"
  
class RecipeRequirementUpdate(LoginRequiredMixin, UpdateView):
  model = RecipeRequirement
  template_name = "inventory/reciperequirement_update_form.html"
  form_class = RecipeRequirementForm
  success_url: "menuitem/list"

class PurchaseList(LoginRequiredMixin, ListView):
  model = Purchase
  template_name = "inventory/purchase_list.html"

class PurchaseCreate(LoginRequiredMixin, CreateView):
  model = Purchase
  form_class = PurchaseForm
  template_name = "inventory/purchase_create.html"

  # decreasing ingredient.quantity because ingredients were used for the purchased menu_item.
  def post(self, request):
    menu_item_id = request.POST["menu_item"]
    menu_item = MenuItem.objects.get(pk=menu_item_id)
    requirements = menu_item.reciperequirement_set
    purchase = Purchase(menu_item=menu_item)

    for requirement in requirements.all():
        required_ingredient = requirement.ingredient
        required_ingredient.quantity -= requirement.quantity
        required_ingredient.save()

    purchase.save()
    return redirect("/purchase/list")
    
#Define a view function in your Django views file.
#Use the Purchase model to retrieve the required data.
#Calculate the cost, revenue, and profit using the methods defined in the Purchase model.
#Pass the calculated values to a template for rendering.

def show_profit(request):
    # Retrieve all purchases from the database
    purchases = Purchase.objects.all()

    # Initialize variables to store total cost, revenue, and profit
    total_cost = 0
    total_revenue = 0
    total_profit = 0

    # Calculate total cost, revenue, and profit for all purchases
    for purchase in purchases:
        total_cost += purchase.get_cost()
        total_revenue += purchase.get_revenue()
        total_profit += purchase.get_profit()

    total_cost = round(total_cost, 2)
    total_revenue = round(total_revenue, 2)
    total_profit = round(total_profit, 2)

    # Pass the calculated values to the template
    context = {
        'total_cost': total_cost,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
    }

    return render(request, 'inventory/balance.html', context)
 
