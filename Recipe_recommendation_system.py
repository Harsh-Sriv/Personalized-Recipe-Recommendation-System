import psycopg2
import json
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
    
    def load_recipe_data(self):
        """Load recipe data from the database into a pandas DataFrame"""
        try:
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
            
            # Create text representation for ingredients and categories
            self.recipe_df['ingredients_text'] = self.recipe_df['ingredients'].apply(
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
    
    def recommend_recipes_by_ingredients(self, ingredients_list, top_n=5, max_calories=None):
        """Recommend recipes based on a list of ingredients with calorie constraint"""
        try:
            # Create a text representation of the input ingredients
            ingredients_text = ' '.join(ingredients_list)
            
            # Convert to a vector using the same vectorizer
            vectorizer = TfidfVectorizer(stop_words='english')
            all_ingredients_text = list(self.recipe_df['ingredients_text']) + [ingredients_text]
            ingredients_matrix = vectorizer.fit_transform(all_ingredients_text)
            
            # Get the input vector
            input_vector = ingredients_matrix[-1]
            
            # Calculate cosine similarity with all recipes
            similarities = cosine_similarity(input_vector, ingredients_matrix[:-1]).flatten()
            
            # Create a DataFrame with recipe indices and similarity scores
            similarity_df = pd.DataFrame({
                'index': range(len(similarities)),
                'similarity': similarities
            })
            
            # Filter by calories if specified
            if max_calories is not None and max_calories > 0:
                # Get indices of recipes that meet the calorie constraint
                valid_indices = self.recipe_df[self.recipe_df['calories'] <= max_calories].index
                similarity_df = similarity_df[similarity_df['index'].isin(valid_indices)]
            
            # Sort by similarity score and get top N
            similarity_df = similarity_df.sort_values('similarity', ascending=False).head(top_n)
            
            # Get recipe details
            similar_recipes_with_scores = []
            for _, row in similarity_df.iterrows():
                idx = row['index']
                recipe = self.recipe_df.iloc[idx].to_dict()
                recipe['similarity_score'] = row['similarity']
                similar_recipes_with_scores.append(recipe)
            
            return similar_recipes_with_scores
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
            # Flatten the list of ingredients from all recipes
            all_ingredients = []
            for ingredients in self.recipe_df['ingredients']:
                if isinstance(ingredients, list):
                    all_ingredients.extend(ingredients)
            
            # Count occurrences of each ingredient
            ingredient_counts = {}
            for ingredient in all_ingredients:
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
    print("Please enter the ingredients you have (comma-separated):")
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

def display_recipe(recipe):
    """Display recipe details in a formatted way"""
    print(f"\n{'=' * 50}")
    print(f"Recipe: {recipe['title']}")
    print(f"{'=' * 50}")
    print(f"Similarity Score: {recipe['similarity_score']:.2f}")
    print(f"Calories: {recipe['calories']}")
    print(f"Cooking Time: {recipe['total_mins']} minutes")
    print(f"Rating: {recipe['ratings']}")
    
    print("\nIngredients:")
    if isinstance(recipe['ingredients'], list):
        for i, ingredient in enumerate(recipe['ingredients'], 1):
            print(f"  {i}. {ingredient}")
    
    print("\nCategories:")
    if isinstance(recipe['category'], list):
        print(f"  {', '.join(recipe['category'])}")
    
    print(f"{'=' * 50}")

def main():
    # Database connection parameters
    DB_NAME = "recipe_chatbot"
    DB_USER = "postgres"  # Replace with your PostgreSQL username
    DB_PASSWORD = "1234"  # Replace with your PostgreSQL password
    DB_HOST = "localhost"
    DB_PORT = "5432"
    
    # Create and initialize the recommender
    recommender = RecipeRecommender(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    if recommender.initialize_recommender():
        try:
            # Get user input
            ingredients, max_calories, count = get_user_input()
            
            # Display what the system is doing
            print(f"\nSearching for recipes with: {', '.join(ingredients)}")
            if max_calories:
                print(f"Maximum calories: {max_calories}")
            print("Finding the best matches...\n")
            
            # Get recommendations
            recommended_recipes = recommender.recommend_recipes_by_ingredients(
                ingredients, top_n=count, max_calories=max_calories
            )
            
            if recommended_recipes:
                print(f"Found {len(recommended_recipes)} recipe(s) matching your criteria:")
                for i, recipe in enumerate(recommended_recipes, 1):
                    print(f"{i}. {recipe['title']} (Similarity: {recipe['similarity_score']:.2f}, Calories: {recipe['calories']})")
                
                # Ask user which recipe they want to see in detail
                print("\nEnter the number of the recipe you'd like to see in detail (or 0 to exit):")
                selection = input("> ")
                
                try:
                    selection = int(selection)
                    if 1 <= selection <= len(recommended_recipes):
                        display_recipe(recommended_recipes[selection - 1])
                except ValueError:
                    print("Invalid selection.")
            else:
                print("No recipes found matching your criteria.")
                
        finally:
            recommender.disconnect()

if __name__ == "__main__":
    main()