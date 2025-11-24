from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class UserProfile(models.Model):
    """Extended user profile with preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)
    recipes_per_page = models.IntegerField(default=9, validators=[MinValueValidator(6), MaxValueValidator(24)])
    theme_preference = models.CharField(
        max_length=10,
        choices=[('auto', 'Auto'), ('light', 'Light'), ('dark', 'Dark')],
        default='auto'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Category(models.Model):
    """Recipe categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model"""
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text="List ingredients, one per line")
    instructions = models.TextField(help_text="Step-by-step cooking instructions")
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField()
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='recipes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})

    def calculate_average_rating(self):
        """Calculate and update average rating"""
        ratings = self.ratings.all()
        if ratings.exists():
            avg = sum(rating.rating for rating in ratings) / ratings.count()
            self.average_rating = round(avg, 2)
            self.save(update_fields=['average_rating'])
        return self.average_rating


class Comment(models.Model):
    """Comments on recipes"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.recipe.title}"


class Rating(models.Model):
    """Ratings for recipes"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['recipe', 'user']  # One rating per user per recipe
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.title} {self.rating}/5"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.calculate_average_rating()