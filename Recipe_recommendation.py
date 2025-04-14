import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re
import traceback

class RecipeRecommender:
    def __init__(self, csv_path='recipe_dataset_200_with_instructions.csv'):
        self.csv_path = csv_path
        self.recipe_df = None
        
    def load_recipe_data(self):
        """Load recipe data from CSV file into a pandas DataFrame"""
        try:
            # Read the CSV file
            self.recipe_df = pd.read_csv(self.csv_path)
            
            # Process ingredients text for matching
            self.recipe_df['ingredients_clean'] = self.recipe_df['ingredients'].apply(
                lambda x: [ing.strip('"') for ing in eval(x) if ing]
            )
            
            # Convert ratings to float
            self.recipe_df['rating'] = pd.to_numeric(self.recipe_df['ratings'], errors='coerce')
            
            # Convert calories and total_mins to numeric
            self.recipe_df['calories'] = pd.to_numeric(self.recipe_df['calories'], errors='coerce')
            self.recipe_df['total_mins'] = pd.to_numeric(self.recipe_df['total_mins'], errors='coerce')
            
            print(f"Loaded {len(self.recipe_df)} recipes successfully!")
            return True
        except Exception as e:
            print(f"Error loading recipe data: {str(e)}")
            traceback.print_exc()
            return False
    
    def recommend_recipes_by_ingredients(self, ingredients, max_calories=None, dietary_restrictions=None, max_time=None, difficulty=None):
        """
        Recommend recipes based on available ingredients and constraints
        """
        try:
            if self.recipe_df is None:
                if not self.load_recipe_data():
                    return []

            # Clean and normalize input ingredients
            cleaned_ingredients = [ing.lower().strip() for ing in ingredients]
            
            # Filter recipes based on constraints
            filtered_df = self.recipe_df.copy()
            
            if max_calories:
                filtered_df = filtered_df[filtered_df['calories'] <= max_calories]
            
            if max_time:
                filtered_df = filtered_df[filtered_df['total_mins'] <= max_time]
            
            if dietary_restrictions:
                for restriction in dietary_restrictions:
                    if restriction == 'vegetarian':
                        filtered_df = filtered_df[filtered_df['category'].apply(lambda x: 'Vegetarian' in eval(x) if isinstance(x, str) else False)]
                    elif restriction == 'vegan':
                        filtered_df = filtered_df[filtered_df['category'].apply(lambda x: 'Vegan' in eval(x) if isinstance(x, str) else False)]
                    elif restriction == 'gluten-free':
                        filtered_df = filtered_df[filtered_df['category'].apply(lambda x: 'Gluten-Free' in eval(x) if isinstance(x, str) else False)]
            
            # Calculate recipe scores based on ingredient matches
            recipe_scores = []
            for _, recipe in filtered_df.iterrows():
                recipe_ingredients = [ing.lower() for ing in recipe['ingredients_clean']]
                matching_ingredients = set(cleaned_ingredients) & set(recipe_ingredients)
                
                # Calculate score based on ingredient matches and recipe rating
                match_score = len(matching_ingredients) / len(cleaned_ingredients)
                rating_score = float(recipe['rating']) / 5.0 if pd.notna(recipe['rating']) else 0.5
                
                # Combine scores with weights
                total_score = (0.7 * match_score) + (0.3 * rating_score)
                
                recipe_scores.append({
                    'recipe_id': recipe['recipe_id'],
                    'title': recipe['title'],
                    'score': total_score,
                    'matching_ingredients': list(matching_ingredients),
                    'calories': float(recipe['calories']) if pd.notna(recipe['calories']) else None,
                    'total_mins': int(recipe['total_mins']) if pd.notna(recipe['total_mins']) else None,
                    'rating': float(recipe['rating']) if pd.notna(recipe['rating']) else None,
                    'image_url': recipe.get('image_url', '')
                })
            
            # Sort recipes by score and return top 10
            recipe_scores.sort(key=lambda x: x['score'], reverse=True)
            return recipe_scores[:10]
            
        except Exception as e:
            print(f"Error in recommend_recipes_by_ingredients: {str(e)}")
            traceback.print_exc()
            return []
    
    def get_recipe_details(self, recipe_id):
        """
        Get detailed information about a specific recipe
        """
        try:
            if self.recipe_df is None:
                if not self.load_recipe_data():
                    return None

            # Find the recipe in the DataFrame
            recipe = self.recipe_df[self.recipe_df['recipe_id'] == recipe_id]
            if recipe.empty:
                print(f"Recipe with ID {recipe_id} not found")
                return None

            recipe = recipe.iloc[0]
            
            # Convert recipe data to a dictionary with proper type handling
            recipe_details = {
                'recipe_id': recipe['recipe_id'],
                'title': recipe['title'],
                'description': recipe.get('instructions', ''),
                'ingredients': recipe['ingredients_clean'],
                'instructions': recipe.get('instructions', '').split('\n') if pd.notna(recipe.get('instructions')) else [],
                'calories': float(recipe['calories']) if pd.notna(recipe['calories']) else None,
                'total_mins': int(recipe['total_mins']) if pd.notna(recipe['total_mins']) else None,
                'rating': float(recipe['rating']) if pd.notna(recipe['rating']) else None,
                'image_url': recipe.get('image_url', ''),
                'categories': eval(recipe['category']) if pd.notna(recipe['category']) else []
            }

            return recipe_details

        except Exception as e:
            print(f"Error in get_recipe_details: {str(e)}")
            traceback.print_exc()
            return None
    
    def get_common_ingredients(self, min_frequency=5):
        """Get a list of common ingredients from the dataset"""
        try:
            # Flatten all ingredients lists
            all_ingredients = []
            for ingredients in self.recipe_df['ingredients_clean']:
                all_ingredients.extend(ingredients)
            
            # Count ingredient frequencies
            ingredient_counts = pd.Series(all_ingredients).value_counts()
            
            # Filter by minimum frequency
            common_ingredients = ingredient_counts[ingredient_counts >= min_frequency].index.tolist()
            
            return sorted(common_ingredients)
            
        except Exception as e:
            print(f"Error getting common ingredients: {str(e)}")
            traceback.print_exc()
            return []

def get_user_input():
    """Get ingredient and calorie inputs from the user"""
    print("\n=== Recipe Recommendation System ===")
    
    # Option 1: Let users select from common ingredients
    print("How would you like to enter ingredients?")
    print("1. Type in your ingredients")
    print("2. Select from common ingredients")
    choice = input("> ")
    
    ingredients_list = []
    
    if choice == "2":
        # Initialize recommender to get common ingredients
        recommender = initialize_recommender()
        if recommender:
            common_ingredients = recommender.get_common_ingredients()
            recommender.disconnect()
            
            print("\nCommon ingredients (enter numbers, separated by commas):")
            for i, ingredient in enumerate(common_ingredients, 1):
                print(f"{i}. {ingredient}")
            
            selections = input("> ")
            try:
                selected_indices = [int(idx.strip()) for idx in selections.split(",")]
                ingredients_list = [common_ingredients[idx-1] for idx in selected_indices if 1 <= idx <= len(common_ingredients)]
            except ValueError:
                print("Invalid selection. Please enter numbers separated by commas.")
    else:
        print("\nPlease enter the ingredients you have (comma-separated):")
        ingredients_input = input("> ")
        ingredients_list = [ingredient.strip() for ingredient in ingredients_input.split(',')]
    
    print("\nEnter maximum calories (leave empty for no limit):")
    calories_input = input("> ")
    max_calories = None
    if calories_input.strip():
        try:
            max_calories = float(calories_input)
        except ValueError:
            print("Invalid calorie input, using no limit.")
    
    print("\nEnter maximum cooking time (leave empty for no limit):")
    time_input = input("> ")
    max_time = None
    if time_input.strip():
        try:
            max_time = float(time_input)
        except ValueError:
            print("Invalid time input, using no limit.")
    
    print("\nEnter difficulty (leave empty for no preference):")
    difficulty_input = input("> ")
    difficulty = None
    if difficulty_input.strip():
        difficulty = difficulty_input.strip()
    
    print("\nEnter dietary restrictions (comma-separated, leave empty if none):")
    restrictions_input = input("> ")
    dietary_restrictions = None
    if restrictions_input.strip():
        dietary_restrictions = [restriction.strip() for restriction in restrictions_input.split(',')]
    
    print("\nHow many recipe recommendations would you like?")
    count_input = input("> ")
    count = 5  # Default
    if count_input.strip():
        try:
            count = int(count_input)
        except ValueError:
            print("Invalid count, using default of 5.")
    
    return ingredients_list, max_calories, count, max_time, difficulty, dietary_restrictions

def display_recipe(recipe, user_ingredients):
    """Display recipe details in a formatted way with ingredient availability"""
    print(f"\n{'=' * 80}")
    print(f"Recipe: {recipe['title']}")
    print(f"{'=' * 80}")
    
    if 'match_count' in recipe:
        match_percent = (recipe['match_count'] / recipe['total_ingredients']) * 100
        print(f"Ingredient Match: {recipe['match_count']}/{recipe['total_ingredients']} ({match_percent:.1f}%)")
        print(f"Missing Ingredients: {recipe['missing_count']}")
    
    print(f"Calories: {recipe['calories']} per serving")
    print(f"Cooking Time: {recipe['total_mins']} minutes")
    print(f"Rating: {recipe['ratings']}")
    
    # Display matched ingredients with original quantities
    print("\nIngredients You Have:")
    if 'matched_ingredients' in recipe and recipe['matched_ingredients']:
        for i, ingredient in enumerate(recipe['matched_ingredients'], 1):
            print(f"  {i}. {ingredient}")
    else:
        print("  None")
    
    # Display missing ingredients with original quantities
    print("\nIngredients You Need to Buy:")
    if 'missing_ingredients' in recipe and recipe['missing_ingredients']:
        for i, ingredient in enumerate(recipe['missing_ingredients'], 1):
            print(f"  {i}. {ingredient}")
    else:
        print("  None")
    
    # Display all ingredients with status
    print("\nAll Ingredients:")
    if isinstance(recipe['original_ingredients'], list):
        # Clean user ingredients for comparison
        user_ingredients_clean = [self.extract_ingredient_name(ing.lower()) for ing in user_ingredients]
        
        # Display ingredients with availability status
        for i, full_ingredient in enumerate(recipe['original_ingredients'], 1):
            # Extract base ingredient name for matching
            base_ingredient = recipe['ingredients_clean'][i-1] if i-1 < len(recipe['ingredients_clean']) else ""
            
            # Check if ingredient is available
            is_available = base_ingredient.lower() in user_ingredients_clean
            status = "✓" if is_available else "✗"
            print(f"  {i}. {full_ingredient} [{status}]")
    
    print("\nCategories:")
    if isinstance(recipe['category'], list):
        print(f"  {', '.join(recipe['category'])}")
    
    print(f"{'=' * 80}")

def extract_ingredient_name(ingredient_with_quantity):
    """Extract the base ingredient name from a string with quantity.
    Standalone function for use outside the class.
    """
    # Strip any quotes
    ingredient = ingredient_with_quantity.strip('"\'')
    
    # Remove quantities like "1 cup", "2 tablespoons", etc.
    pattern = r'^(\d+\.?\d*|\d+/\d+)?\s*([a-zA-Z]+\s)?(cups?|tablespoons?|teaspoons?|pounds?|ounces?|oz\.?|lbs\.?|tbsp\.?|tsp\.?|g\.?|kg\.?|ml\.?|l\.?|inch(?:es)?|cm|mm|pinch(?:es)?|dash(?:es)?|to taste|large|medium|small)?\s+'
    ingredient_name = re.sub(pattern, '', ingredient, flags=re.IGNORECASE)
    
    # Handle common ingredients with multiple words
    multi_word_ingredients = [
        "all-purpose flour", "olive oil", "vegetable oil", "baking powder",
        "baking soda", "brown sugar", "coconut oil", "cream cheese"
    ]
    
    for multi_word in multi_word_ingredients:
        if multi_word in ingredient.lower():
            return multi_word
    
    # Split and take the last word (usually the main ingredient)
    words = ingredient_name.split()
    if words:
        # Check for compound ingredients
        if "," in ingredient_name or " and " in ingredient_name.lower():
            return ingredient_name
        else:
            # For most cases, take the last meaningful word
            last_word = words[-1].lower()
            if len(last_word) > 1:
                return last_word
            elif len(words) > 1:
                return words[-2].lower()
    
    return ingredient_name.lower()

def initialize_recommender():
    """Initialize the recommender with database connection parameters"""
    # Database connection parameters
    DB_NAME = "recipe_chatbot"
    DB_USER = "postgres"  # Replace with your PostgreSQL username
    DB_PASSWORD = "1234"  # Replace with your PostgreSQL password
    DB_HOST = "localhost"
    DB_PORT = "5432"
    
    # Create and initialize the recommender
    recommender = RecipeRecommender(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    if recommender.initialize_recommender():
        return recommender
    return None

def main():
    # Initialize the recommender
    recommender = initialize_recommender()
    if recommender:
        try:
            # Get user input
            user_ingredients, max_calories, count, max_time, difficulty, dietary_restrictions = get_user_input()
            
            # Display what the system is doing
            print(f"\nSearching for recipes with: {', '.join(user_ingredients)}")
            if max_calories:
                print(f"Maximum calories: {max_calories}")
            if max_time:
                print(f"Maximum cooking time: {max_time} minutes")
            if difficulty:
                print(f"Difficulty: {difficulty}")
            if dietary_restrictions:
                print(f"Dietary Restrictions: {', '.join(dietary_restrictions)}")
            print("Finding the best matches based on ingredient availability...\n")
            
            # Get recommendations based on ingredient matching
            recommended_recipes = recommender.recommend_recipes_by_ingredients(
                user_ingredients, max_calories=max_calories, max_time=max_time, difficulty=difficulty, dietary_restrictions=dietary_restrictions
            )
            
            if recommended_recipes:
                print(f"Found {len(recommended_recipes)} recipe(s) matching your criteria:")
                print(f"{'=' * 80}")
                print(f"{'#':<3} {'Recipe Title':<40} {'Match':<7} {'Missing':<8} {'Match %':<8}")
                print(f"{'=' * 80}")
                
                for i, recipe in enumerate(recommended_recipes, 1):
                    match_percent = (recipe['match_count'] / recipe['total_ingredients']) * 100
                    print(f"{i:<3} {recipe['title'][:38]:<40} {recipe['match_count']}/{recipe['total_ingredients']:<7} {recipe['missing_count']:<8} {match_percent:.1f}%")
                
                # Ask user which recipe they want to see in detail
                while True:
                    print("\nEnter the number of the recipe you'd like to see in detail (or 0 to exit):")
                    selection = input("> ")
                    
                    try:
                        selection = int(selection)
                        if selection == 0:
                            break
                        elif 1 <= selection <= len(recommended_recipes):
                            display_recipe(recommended_recipes[selection - 1], user_ingredients)
                        else:
                            print("Invalid selection. Please try again.")
                    except ValueError:
                        print("Invalid selection. Please enter a number.")
            else:
                print("No recipes found matching your criteria.")
                
        finally:
            recommender.disconnect()

if __name__ == "__main__":
    main()