from users.models import GroceryCategory

def populate_categories():
    # List of categories to add
    if GroceryCategory.objects.all().exists():
        print("Categories already exist.")
        return
    else:
        categories = [
            "Fruits", "Vegetables", "Dairy", "Meat", "Seafood",
            "Grains", "Pasta", "Baking Supplies", "Spices",
            "Beverages", "Snacks", "Frozen Foods", "Cleaning Products",
            "Toiletries", "Baby Food", "Pet Food", "Health Supplements",
            "Canned Goods", "Condiments", "Sauces", "Breakfast Cereals",
            "Nuts and Seeds", "Herbs", "Cooking Oils", "Sweets and Desserts"
        ]

        # Create categories if they don't already exist
        for category in categories:
            category, created = GroceryCategory.objects.get_or_create(category_name=category.lower())
            if created:
                print(f"Added category: {category.category_name.capitalize()}")
            else:
                print(f"Category already exists: {category.category_name.capitalize()}")

if __name__ == "__main__":
    populate_categories()