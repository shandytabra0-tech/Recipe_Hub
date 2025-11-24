from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category


class Command(BaseCommand):
    help = 'Create sample admin recipes'

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@recipehub.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Get categories
        main_course = Category.objects.get(name__icontains='Main Course')
        desserts = Category.objects.get(name__icontains='Desserts')
        breakfast = Category.objects.get(name__icontains='Breakfast')
        
        admin_recipes = [
            {
                'title': 'Classic Spaghetti Carbonara',
                'description': 'A traditional Italian pasta dish with eggs, cheese, and pancetta. Simple yet elegant.',
                'ingredients': '''400g spaghetti
200g pancetta or guanciale, diced
4 large eggs
100g Pecorino Romano cheese, grated
50g Parmesan cheese, grated
Black pepper, freshly ground
Salt for pasta water''',
                'instructions': '''Bring a large pot of salted water to boil and cook spaghetti according to package directions.
While pasta cooks, heat a large skillet over medium heat and cook pancetta until crispy.
In a bowl, whisk together eggs, Pecorino Romano, Parmesan, and plenty of black pepper.
Reserve 1 cup pasta cooking water, then drain pasta.
Add hot pasta to the skillet with pancetta and toss.
Remove from heat and quickly stir in egg mixture, adding pasta water as needed.
Serve immediately with extra cheese and black pepper.''',
                'prep_time': 15,
                'cook_time': 20,
                'servings': 4,
                'category': main_course,
                'status': 'approved'
            },
            {
                'title': 'Decadent Chocolate Lava Cake',
                'description': 'Rich, molten chocolate cake with a gooey center. Perfect for special occasions.',
                'ingredients': '''100g dark chocolate (70% cocoa)
100g unsalted butter
2 large eggs
2 large egg yolks
60g caster sugar
2 tbsp plain flour
Butter for ramekins
Cocoa powder for dusting
Vanilla ice cream for serving''',
                'instructions': '''Preheat oven to 200°C. Butter 4 ramekins and dust with cocoa powder.
Melt chocolate and butter in a double boiler until smooth.
In a bowl, whisk eggs, egg yolks, and sugar until thick and pale.
Fold in melted chocolate mixture, then gently fold in flour.
Divide mixture between ramekins and place on a baking tray.
Bake for 12-14 minutes until edges are firm but centers still jiggle.
Let cool for 1 minute, then run a knife around edges and invert onto plates.
Serve immediately with vanilla ice cream.''',
                'prep_time': 20,
                'cook_time': 14,
                'servings': 4,
                'category': desserts,
                'status': 'approved'
            },
            {
                'title': 'Perfect Fluffy Pancakes',
                'description': 'Light, fluffy pancakes that are perfect for weekend breakfast or brunch.',
                'ingredients': '''200g plain flour
2 tsp baking powder
1 tsp salt
2 tbsp caster sugar
2 large eggs
300ml whole milk
50g melted butter
1 tsp vanilla extract
Butter for cooking
Maple syrup for serving''',
                'instructions': '''In a large bowl, whisk together flour, baking powder, salt, and sugar.
In another bowl, whisk eggs, then add milk, melted butter, and vanilla.
Pour wet ingredients into dry ingredients and stir until just combined (lumps are okay).
Let batter rest for 5 minutes while heating a non-stick pan over medium heat.
Brush pan with butter and pour 1/4 cup batter for each pancake.
Cook until bubbles form on surface and edges look set, about 2-3 minutes.
Flip and cook until golden brown, another 1-2 minutes.
Serve hot with butter and maple syrup.''',
                'prep_time': 10,
                'cook_time': 15,
                'servings': 4,
                'category': breakfast,
                'status': 'approved'
            }
        ]
        
        created_count = 0
        for recipe_data in admin_recipes:
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                author=admin_user,
                defaults=recipe_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created recipe: {recipe.title}')
        
        self.stdout.write(f'Successfully created {created_count} admin recipes')