from django.core.management.base import BaseCommand
from recipes.models import Category


class Command(BaseCommand):
    help = 'Update category names with emojis'

    def handle(self, *args, **options):
        category_updates = {
            'Appetizers': '🥗 Appetizers',
            'Main Course': '🍖 Main Course', 
            'Desserts': '🍰 Desserts',
            'Beverages': '🥤 Beverages',
            'Breakfast': '🥞 Breakfast',
            'Lunch': '🥙 Lunch',
            'Dinner': '🍽️ Dinner',
            'Snacks': '🍿 Snacks',
            'Vegetarian': '🥬 Vegetarian',
            'Vegan': '🌱 Vegan',
            'Gluten-Free': '🌾 Gluten-Free',
            'Healthy': '💚 Healthy',
            'Quick & Easy': '⚡ Quick & Easy',
            'Comfort Food': '🏠 Comfort Food',
            'International': '🌍 International',
        }

        updated_count = 0
        for old_name, new_name in category_updates.items():
            try:
                category = Category.objects.get(name=old_name)
                category.name = new_name
                category.save()
                updated_count += 1
                self.stdout.write(f'Updated: {old_name} to {new_name}')
            except Category.DoesNotExist:
                pass

        self.stdout.write(f'Successfully updated {updated_count} categories')