from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('submit/', views.submit_recipe, name='submit_recipe'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='recipes/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]

