from django.urls import path, include
from . import views

urlpatterns = [
  path("registration/", include("django.contrib.auth.urls")),
  path("registration/login", views.UserLogin.as_view(), name = "login"),
  path("registration/profile", views.UserProfile, name = "profile"),
  path("registration/resetpassword", views.UserResetPassword, name = "reset_password"),
  path("signup/", views.SignUp.as_view(), name = 'signup'),
  path("logout", views.logout_view, name="logout"),
  path("", views.home, name="home"),
  path("ingredient/list", views.IngredientList.as_view(), name="ingredientlist"),
  path("ingredient/create", views.IngredientCreate.as_view(), name="ingredientcreate"),
  path("ingredient/<pk>", views.IngredientDetail.as_view(), name="ingredientdetails"),
  path("ingredient/<pk>/update", views.IngredientUpdate.as_view(), name="ingredientupdate"),
  path("ingredient/<pk>/delete", views.IngredientDelete.as_view(), name="ingredientdelete"),
  path("menuitem/list", views.MenuItemList.as_view(), name="menuitemlist"),
  path("menuitem/create", views.MenuItemCreate.as_view(), name="menuitemcreate"),
  path("menuitem/<pk>", views.MenuItemDetail.as_view(), name="menuitemdetails"),
  path("menuitem/<pk>/update", views.MenuItemUpdate.as_view(), name="menuitemupdate"),
  path("menuitem/<pk>/delete", views.MenuItemDelete.as_view(), name='menuitemdelete'),
  path("purchase/list", views.PurchaseList.as_view(), name="purchaselist"),
  path("purchase/create", views.PurchaseCreate.as_view(), name="purchasecreate"),
  path('balance/', views.show_profit, name='show_profit'),
  path("reciperequirement/create", views.RecipeRequirementCreate.as_view(), name="recreqcreate"),
  path("reciperequirement/<pk>/update", views.RecipeRequirementUpdate.as_view(), name="recrequpdate"),
]