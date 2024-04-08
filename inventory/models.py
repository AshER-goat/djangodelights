from django.db import models

class Ingredient(models.Model):
    POUND = "LB"
    TEASPOON = "TSP"
    TABLESPOON = "TBSP"
    CUP = "CUP"
    OUNCE = "OZ"
    PINT = "PINT"
    QUART = "QT"
    GALLON = "GAL"
    GRAM = "GRAM"
    COUNT = "CNT"

    UNIT_TYPE_CHOICES = [
        (TEASPOON, "Teaspoon"),
        (TABLESPOON, "Tablespoon"),
        (CUP, "Cup"),
        (OUNCE, "Ounce"),
        (PINT, "Pint"),
        (QUART, "Quart"),
        (GALLON, "Gallon"),
        (POUND, "Pound"),
        (GRAM, "Gram"),
        (COUNT, "Count"),
    ]
    name = models.CharField(max_length=64)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)    #.FloatField(default=0.5)
    unit = models.CharField(max_length=4, choices=UNIT_TYPE_CHOICES, default=POUND)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)    #.FloatField(default=0.5)

    def __str__(self):
        return f"{self.name} ({self.unit})"
        
    def get_absolute_url(self):
        return "/ingredient/list"


class MenuItem(models.Model):
    title = models.CharField(max_length=128)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    
    def __str__(self):
        return f"{self.title} at ${self.price}"

    def get_absolute_url(self):
        return "/menuitem/list"


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=1, max_digits=4)

    def get_absolute_url(self):
        return "/menuitem/list"


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/purchase/list"

    #total cost of menu item ingredients
    def get_cost(self):
        recipe_objects = RecipeRequirement.objects.filter(menu_item=self.menu_item)
        return sum([z.ingredient.unit_price * z.quantity for z in recipe_objects])

    #total price of the menu items sold
    def get_revenue(self):
        return self.menu_item.price

    #profit
    def get_profit(self):
        return float(self.get_revenue()) - float(self.get_cost())