from django.core.management.base import BaseCommand
from recipes.models import Category


class Command(BaseCommand):
    help = 'Create default recipe categories'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Appetizers', 'description': 'Starters and small bites'},
            {'name': 'Main Course', 'description': 'Primary dishes and entrees'},
            {'name': 'Desserts', 'description': 'Sweet treats and desserts'},
            {'name': 'Beverages', 'description': 'Drinks and cocktails'},
            {'name': 'Breakfast', 'description': 'Morning meals and brunch'},
            {'name': 'Lunch', 'description': 'Midday meals'},
            {'name': 'Dinner', 'description': 'Evening meals'},
            {'name': 'Snacks', 'description': 'Quick bites and snacks'},
            {'name': 'Vegetarian', 'description': 'Plant-based recipes'},
            {'name': 'Vegan', 'description': 'Completely plant-based recipes'},
            {'name': 'Gluten-Free', 'description': 'Recipes without gluten'},
            {'name': 'Healthy', 'description': 'Nutritious and balanced meals'},
            {'name': 'Quick & Easy', 'description': 'Fast recipes under 30 minutes'},
            {'name': 'Comfort Food', 'description': 'Hearty and satisfying dishes'},
            {'name': 'International', 'description': 'Recipes from around the world'},
        ]

        created_count = 0
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} categories')
        )