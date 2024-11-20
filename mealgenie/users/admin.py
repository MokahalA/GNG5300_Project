from django.contrib import admin
from users.models import UserProfile, GroceryCategory, Grocery, UserGrocery

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dietary_preferences', 'allergies']

class GroceryCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']

class GroceryAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'unit']

class UserGroceryAdmin(admin.ModelAdmin):
    list_display = ['user', 'grocery', 'quantity', 'expiration_date']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GroceryCategory, GroceryCategoryAdmin)
admin.site.register(Grocery, GroceryAdmin)
admin.site.register(UserGrocery, UserGroceryAdmin)
