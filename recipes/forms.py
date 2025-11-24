from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Comment, Rating, Category, UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 
                  'prep_time', 'cook_time', 'servings', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of your delicious recipe'}),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 8, 
                'placeholder': '2 cups all-purpose flour\n1 tsp baking powder\n1/2 cup sugar\n3 large eggs\n1 cup milk'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 10, 
                'placeholder': 'Preheat oven to 350°F (175°C)\nMix dry ingredients in a large bowl\nIn another bowl, whisk eggs and milk\nCombine wet and dry ingredients\nBake for 25-30 minutes until golden'
            }),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Minutes'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Minutes'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Number of servings'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['ingredients'].required = True
        self.fields['instructions'].required = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'type': 'range',
                'step': 1
            })
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date', 'avatar', 'email_notifications', 
                  'show_email', 'recipes_per_page', 'theme_preference']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recipes_per_page': forms.NumberInput(attrs={'class': 'form-control', 'min': 6, 'max': 24}),
            'theme_preference': forms.Select(attrs={'class': 'form-select'}),
        }


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

