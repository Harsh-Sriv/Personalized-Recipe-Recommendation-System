import psycopg2
import json
import re
import numpy as np
import pandas as pd
from psycopg2.extras import RealDictCursor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecipeRecommender:
    def __init__(self, db_name, db_user, db_password, db_host='localhost', db_port='5432'):
        self.connection_params = {
            'dbname': db_name,
            'user': db_user,
            'password': db_password,
            'host': db_host,
            'port': db_port
        }
        self.conn = None
        self.cursor = None
        self.recipe_df = None
        self.ingredient_matrix = None
        self.category_matrix = None
        self.recipe_id_map = {}
        self.inverse_recipe_id_map = {}
        
    def connect(self):
        """Connect to the PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("Connected to the database successfully!")
            return True
        except Exception as e:
            print(f"Error connecting to the database: {str(e)}")
            return False
    
    def disconnect(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")
    
    def extract_ingredient_name(self, ingredient_with_quantity):
        """Extract the base ingredient name from a string with quantity.
        Example: '2 cups all-purpose flour' -> 'flour'
                 '1/2 teaspoon salt' -> 'salt'
        """
        # Strip any quotes
        ingredient = ingredient_with_quantity.strip('"\'')
        
        # Remove quantities like "1 cup", "2 tablespoons", etc.
        # This pattern matches numbers, fractions, and common measurement units
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
        # But avoid single-letter words like "a" or "I"
        words = ingredient_name.split()
        if words:
            # Check for compound ingredients with "and" or commas
            if "," in ingredient_name or " and " in ingredient_name.lower():
                return ingredient_name  # Keep the full string for compound ingredients
            else:
                # For most cases, the main ingredient is the last word
                last_word = words[-1].lower()
                if len(last_word) > 1:  # Avoid single-letter words
                    return last_word
                elif len(words) > 1:
                    return words[-2].lower()
        
        # If all else fails, return the original text
        return ingredient_name.lower()
    
    def load_recipe_data(self):
        """Load recipe data from the database into a pandas DataFrame"""
        try:
            # Modified query to match your actual database schema
            self.cursor.execute("""
                SELECT recipe_id, title, ingredients, category, ratings, reviews, calories, total_mins 
                FROM recipes
            """)
            recipes = self.cursor.fetchall()
            
            # Convert to DataFrame
            self.recipe_df = pd.DataFrame(recipes)
            
            # Create a mapping from recipe_id to matrix index
            for i, recipe_id in enumerate(self.recipe_df['recipe_id']):
                self.recipe_id_map[int(recipe_id)] = i
                self.inverse_recipe_id_map[i] = int(recipe_id)
            
            # Parse JSON strings
            self.recipe_df['ingredients'] = self.recipe_df['ingredients'].apply(
                lambda x: json.loads(x) if isinstance(x, str) else x
            )
            self.recipe_df['category'] = self.recipe_df['category'].apply(
                lambda x: json.loads(x) if isinstance(x, str) else x
            )
            
            # Add original ingredients list (with quantities)
            self.recipe_df['original_ingredients'] = self.recipe_df['ingredients'].copy()
            
            # Extract base ingredient names
            self.recipe_df['ingredients_clean'] = self.recipe_df['ingredients'].apply(
                lambda x: [self.extract_ingredient_name(ing) for ing in x] if isinstance(x, list) else []
            )
            
            # Create text representation for ingredients and categories
            self.recipe_df['ingredients_text'] = self.recipe_df['ingredients_clean'].apply(
                lambda x: ' '.join(x) if isinstance(x, list) else ''
            )
            self.recipe_df['category_text'] = self.recipe_df['category'].apply(
                lambda x: ' '.join(x) if isinstance(x, list) else ''
            )
            
            print(f"Loaded {len(self.recipe_df)} recipes.")
            return True
        except Exception as e:
            print(f"Error loading recipe data: {str(e)}")
            return False
    
    def build_ingredient_matrix(self):
        """Build a TF-IDF matrix for ingredients"""
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            self.ingredient_matrix = vectorizer.fit_transform(self.recipe_df['ingredients_text'])
            print("Ingredient similarity matrix built.")
            return True
        except Exception as e:
            print(f"Error building ingredient matrix: {str(e)}")
            return False
    
    def build_category_matrix(self):
        """Build a TF-IDF matrix for categories"""
        try:
            vectorizer = TfidfVectorizer()
            self.category_matrix = vectorizer.fit_transform(self.recipe_df['category_text'])
            print("Category similarity matrix built.")
            return True
        except Exception as e:
            print(f"Error building category matrix: {str(e)}")
            return False
    
    def initialize_recommender(self):
        """Initialize the recommender by loading data and building matrices"""
        if self.connect():
            if self.load_recipe_data():
                self.build_ingredient_matrix()
                self.build_category_matrix()
                return True
        return False
    
    def get_similar_recipes_by_ingredients(self, recipe_id, top_n=5):
        """Get similar recipes based on ingredients"""
        try:
            # Convert recipe_id to Python int if it's a numpy.int64
            recipe_id = int(recipe_id)
            
            if recipe_id not in self.recipe_id_map:
                print(f"Recipe ID {recipe_id} not found.")
                return []
            
            recipe_idx = self.recipe_id_map[recipe_id]
            recipe_vector = self.ingredient_matrix[recipe_idx]
            
            # Calculate cosine similarity
            similarities = cosine_similarity(recipe_vector, self.ingredient_matrix).flatten()
            
            # Get indices of top similar recipes (excluding the input recipe)
            similar_indices = similarities.argsort()[:-top_n-1:-1]
            similar_indices = [idx for idx in similar_indices if idx != recipe_idx][:top_n]
            
            # Get recipe details
            similar_recipes_with_scores = []
            for idx in similar_indices:
                recipe = self.recipe_df.iloc[idx].to_dict()
                recipe['similarity_score'] = similarities[idx]
                similar_recipes_with_scores.append(recipe)
            
            return similar_recipes_with_scores
        except Exception as e:
            print(f"Error getting similar recipes: {str(e)}")
            return []
    
    def recommend_recipes_by_ingredients(self, user_ingredients, top_n=5, max_calories=None):
        """Recommend recipes based on a list of ingredients with calorie constraint
        and ingredient matching"""
        try:
            # Clean and normalize user ingredients
            user_ingredients_clean = [self.extract_ingredient_name(ingredient.lower()) for ingredient in user_ingredients]
            
            # Count ingredient matches for each recipe and prepare results
            match_results = []
            
            for idx, row in self.recipe_df.iterrows():
                # Skip if recipe doesn't meet calorie constraint
                if max_calories is not None and max_calories > 0 and row['calories'] > max_calories:
                    continue
                
                # Get recipe ingredients (cleaned base ingredients)
                recipe_ingredients_clean = row['ingredients_clean'] if isinstance(row['ingredients_clean'], list) else []
                
                # Count matching ingredients
                matched_ingredients = set(recipe_ingredients_clean).intersection(set(user_ingredients_clean))
                match_count = len(matched_ingredients)
                
                # Only consider recipes with at least one matching ingredient
                if match_count > 0:
                    # Calculate percentage of recipe ingredients that are available
                    ingredient_match_percent = match_count / len(recipe_ingredients_clean) if recipe_ingredients_clean else 0
                    
                    # Calculate how many ingredients are missing
                    missing_ingredients_clean = list(set(recipe_ingredients_clean) - set(user_ingredients_clean))
                    missing_count = len(missing_ingredients_clean)
                    
                    # Get original ingredients with quantities for matched and missing ingredients
                    matched_ingredients_original = []
                    missing_ingredients_original = []
                    
                    for i, clean_ing in enumerate(row['ingredients_clean']):
                        if clean_ing in matched_ingredients:
                            matched_ingredients_original.append(row['original_ingredients'][i])
                        elif clean_ing in missing_ingredients_clean:
                            missing_ingredients_original.append(row['original_ingredients'][i])
                    
                    # Add to results
                    recipe_data = row.to_dict()
                    recipe_data['match_count'] = match_count
                    recipe_data['missing_count'] = missing_count
                    recipe_data['total_ingredients'] = len(recipe_ingredients_clean)
                    recipe_data['match_percent'] = ingredient_match_percent
                    recipe_data['matched_ingredients'] = matched_ingredients_original
                    recipe_data['missing_ingredients'] = missing_ingredients_original
                    recipe_data['matched_ingredients_clean'] = list(matched_ingredients)
                    recipe_data['missing_ingredients_clean'] = missing_ingredients_clean
                    
                    match_results.append(recipe_data)
            
            # Sort by match percentage (descending)
            match_results.sort(key=lambda x: x['match_percent'], reverse=True)
            
            # Return top N results
            return match_results[:top_n]
        except Exception as e:
            print(f"Error recommending recipes: {str(e)}")
            return []
    
    def get_recipe_details(self, recipe_id):
        """Get detailed information about a recipe"""
        try:
            # Convert recipe_id to Python int if it's a numpy.int64
            recipe_id = int(recipe_id)
            
            if recipe_id not in self.recipe_id_map:
                print(f"Recipe ID {recipe_id} not found.")
                return None
            
            idx = self.recipe_id_map[recipe_id]
            recipe = self.recipe_df.iloc[idx].to_dict()
            
            # Get reviews
            self.cursor.execute("""
                SELECT r.review, r.rating, u.username
                FROM reviews r
                JOIN users u ON r.user_id = u.user_id
                WHERE r.recipe_id = %s
                ORDER BY r.rating DESC
                LIMIT 5
            """, (recipe_id,))
            reviews = self.cursor.fetchall()
            
            recipe['reviews_detail'] = reviews
            
            return recipe
        except Exception as e:
            print(f"Error getting recipe details: {str(e)}")
            return None

    def get_common_ingredients(self):
        """Get a list of common ingredients for user selection"""
        try:
            # Use the cleaned ingredient names for better grouping
            all_ingredients = []
            for ingredients in self.recipe_df['ingredients_clean']:
                if isinstance(ingredients, list):
                    all_ingredients.extend(ingredients)
            
            # Count occurrences of each ingredient
            ingredient_counts = {}
            for ingredient in all_ingredients:
                ingredient = ingredient.lower()
                ingredient_counts[ingredient] = ingredient_counts.get(ingredient, 0) + 1
            
            # Sort ingredients by frequency
            sorted_ingredients = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Return top ingredients (e.g., top 100)
            top_ingredients = [ingredient for ingredient, count in sorted_ingredients[:100]]
            return top_ingredients
        except Exception as e:
            print(f"Error getting common ingredients: {str(e)}")
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
    
    print("\nHow many recipe recommendations would you like?")
    count_input = input("> ")
    count = 5  # Default
    if count_input.strip():
        try:
            count = int(count_input)
        except ValueError:
            print("Invalid count, using default of 5.")
    
    return ingredients_list, max_calories, count

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
        user_ingredients_clean = [extract_ingredient_name(ing.lower()) for ing in user_ingredients]
        
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
            user_ingredients, max_calories, count = get_user_input()
            
            # Display what the system is doing
            print(f"\nSearching for recipes with: {', '.join(user_ingredients)}")
            if max_calories:
                print(f"Maximum calories: {max_calories}")
            print("Finding the best matches based on ingredient availability...\n")
            
            # Get recommendations based on ingredient matching
            recommended_recipes = recommender.recommend_recipes_by_ingredients(
                user_ingredients, top_n=count, max_calories=max_calories
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