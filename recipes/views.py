from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from .models import Recipe, Category, Comment, Rating, UserProfile
from .forms import UserRegistrationForm, RecipeForm, CommentForm, RatingForm, UserProfileForm, UserSettingsForm


def home(request):
    """Homepage displaying recipes with filtering options"""
    # User filter
    user_filter = request.GET.get('user_filter', '')
    
    if user_filter == 'my_recipes' and request.user.is_authenticated:
        # Show only user's own recipes (any status)
        recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    elif request.user.is_authenticated:
        # Show approved recipes + user's own recipes (any status)
        recipes = Recipe.objects.filter(
            Q(status='approved') | Q(author=request.user)
        ).order_by('-created_at')
    else:
        # Show only approved recipes for anonymous users
        recipes = Recipe.objects.filter(status='approved').order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category', '')
    if category_id:
        recipes = recipes.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(recipes, 9)  # Show 9 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all().order_by('name')
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'user_filter': user_filter,
    }
    return render(request, 'recipes/home.html', context)


def recipe_detail(request, pk):
    """Display recipe details with comments and ratings"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Only show approved recipes to non-admin users
    if not request.user.is_staff and recipe.status != 'approved':
        messages.error(request, 'This recipe is not available.')
        return redirect('home')
    
    comments = recipe.comments.all()
    user_rating = None
    
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(recipe=recipe, user=request.user)
        except Rating.DoesNotExist:
            pass
    
    # Handle comment submission
    if request.method == 'POST' and 'comment' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('recipe_detail', pk=recipe.pk)
    
    # Handle rating submission
    if request.method == 'POST' and 'rating' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to rate.')
            return redirect('login')
        
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating, created = Rating.objects.get_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'rating': rating_form.cleaned_data['rating']}
            )
            if not created:
                rating.rating = rating_form.cleaned_data['rating']
                rating.save()
            messages.success(request, 'Your rating has been saved!')
            return redirect('recipe_detail', pk=recipe.pk)
    
    comment_form = CommentForm()
    rating_form = RatingForm()
    
    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
    }
    return render(request, 'recipes/recipe_detail.html', context)


@login_required
def submit_recipe(request):
    """Allow users to submit new recipes"""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.status = 'pending'  # Set to pending for admin approval
            recipe.save()
            messages.success(request, 'Your recipe has been submitted and is pending approval!')
            return redirect('home')
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/submit_recipe.html', {'form': form})


@login_required
def my_recipes(request):
    """Display recipes submitted by the current user with statistics"""
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    
    # Calculate statistics
    approved_count = recipes.filter(status='approved').count()
    pending_count = recipes.filter(status='pending').count()
    rejected_count = recipes.filter(status='rejected').count()
    
    # Calculate average rating
    avg_rating = recipes.filter(average_rating__gt=0).aggregate(
        avg=Avg('average_rating')
    )['avg'] or 0
    
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'avg_rating': avg_rating,
    }
    return render(request, 'recipes/my_recipes.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'recipes/register.html', {'form': form})


def login_view(request):
    """User login"""
    from django.contrib.auth.views import LoginView
    return LoginView.as_view(template_name='recipes/login.html')(request)


def user_profile(request, username):
    """Display user profile with their approved recipes"""
    profile_user = get_object_or_404(User, username=username)
    
    # Show only approved recipes for other users, all recipes for own profile
    if request.user == profile_user:
        recipes = Recipe.objects.filter(author=profile_user).order_by('-created_at')
    else:
        recipes = Recipe.objects.filter(author=profile_user, status='approved').order_by('-created_at')
    
    # Calculate statistics
    total_recipes = recipes.count()
    approved_recipes = Recipe.objects.filter(author=profile_user, status='approved').count()
    avg_rating = recipes.filter(average_rating__gt=0).aggregate(avg=Avg('average_rating'))['avg'] or 0
    
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': profile_user,
        'page_obj': page_obj,
        'total_recipes': total_recipes,
        'approved_recipes': approved_recipes,
        'avg_rating': avg_rating,
    }
    return render(request, 'recipes/user_profile.html', context)


@login_required
def settings(request):
    """User settings and preferences"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserSettingsForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your settings have been updated successfully!')
            return redirect('settings')
    else:
        user_form = UserSettingsForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'recipes/settings.html', context)


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

