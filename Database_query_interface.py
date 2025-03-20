import psycopg2
import json
from psycopg2.extras import RealDictCursor
import pandas as pd

class RecipeDatabase:
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
    
    def get_recipe_by_id(self, recipe_id):
        """Get a recipe by its ID"""
        try:
            self.cursor.execute("""
                SELECT * FROM recipes WHERE recipe_id = %s
            """, (recipe_id,))
            recipe = self.cursor.fetchone()
            return recipe
        except Exception as e:
            print(f"Error retrieving recipe: {str(e)}")
            return None
    
    def search_recipes_by_title(self, title_query, limit=10):
        """Search recipes by title"""
        try:
            self.cursor.execute("""
                SELECT * FROM recipes 
                WHERE title ILIKE %s 
                ORDER BY ratings DESC 
                LIMIT %s
            """, (f"%{title_query}%", limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error searching recipes: {str(e)}")
            return []
    
    def search_recipes_by_ingredient(self, ingredient_query, limit=10):
        """Search recipes by ingredient"""
        try:
            self.cursor.execute("""
                SELECT r.* FROM recipes r
                JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
                JOIN ingredients i ON ri.ingredient_id = i.id
                WHERE i.clean_name ILIKE %s
                ORDER BY r.ratings DESC
                LIMIT %s
            """, (f"%{ingredient_query}%", limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error searching recipes by ingredient: {str(e)}")
            return []
    
    def get_top_rated_recipes(self, limit=10):
        """Get top-rated recipes"""
        try:
            self.cursor.execute("""
                SELECT * FROM recipes 
                ORDER BY ratings DESC, reviews DESC 
                LIMIT %s
            """, (limit,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving top-rated recipes: {str(e)}")
            return []
    
    def get_quick_recipes(self, max_minutes=30, limit=10):
        """Get quick recipes that can be prepared in under the specified time"""
        try:
            self.cursor.execute("""
                SELECT * FROM recipes 
                WHERE total_mins <= %s 
                ORDER BY ratings DESC 
                LIMIT %s
            """, (max_minutes, limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving quick recipes: {str(e)}")
            return []
    
    def get_recipes_by_category(self, category, limit=10):
        """Get recipes by category"""
        try:
            self.cursor.execute("""
                SELECT * FROM recipes 
                WHERE category @> %s 
                ORDER BY ratings DESC 
                LIMIT %s
            """, (json.dumps([category]), limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving recipes by category: {str(e)}")
            return []
    
    def get_recipes_by_calorie_range(self, min_calories, max_calories, limit=10):
        """Get recipes within a calorie range"""
        try:
            self.cursor.execute("""
                SELECT * FROM recipes 
                WHERE calories BETWEEN %s AND %s 
                ORDER BY ratings DESC 
                LIMIT %s
            """, (min_calories, max_calories, limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving recipes by calorie range: {str(e)}")
            return []
    
    def get_user_reviews(self, user_id, limit=10):
        """Get reviews by a specific user"""
        try:
            self.cursor.execute("""
                SELECT r.review, r.rating, r.date, rec.title 
                FROM reviews r
                JOIN recipes rec ON r.recipe_id = rec.recipe_id
                WHERE r.user_id = %s
                LIMIT %s
            """, (user_id, limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving user reviews: {str(e)}")
            return []
    
    def get_recipe_reviews(self, recipe_id, limit=10):
        """Get reviews for a specific recipe"""
        try:
            self.cursor.execute("""
                SELECT r.review, r.rating, r.date, u.username 
                FROM reviews r
                JOIN users u ON r.user_id = u.user_id
                WHERE r.recipe_id = %s
                ORDER BY r.date DESC
                LIMIT %s
            """, (recipe_id, limit))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving recipe reviews: {str(e)}")
            return []

    def get_recipe_stats(self):
        """Get basic statistics about the recipes database"""
        try:
            stats = {}
            
            # Total number of recipes
            self.cursor.execute("SELECT COUNT(*) as total FROM recipes")
            stats['total_recipes'] = self.cursor.fetchone()['total']
            
            # Average rating
            self.cursor.execute("SELECT AVG(ratings) as avg_rating FROM recipes")
            stats['avg_rating'] = self.cursor.fetchone()['avg_rating']
            
            # Average calories
            self.cursor.execute("SELECT AVG(calories) as avg_calories FROM recipes")
            stats['avg_calories'] = self.cursor.fetchone()['avg_calories']
            
            # Average cooking time
            self.cursor.execute("SELECT AVG(total_mins) as avg_cooking_time FROM recipes")
            stats['avg_cooking_time'] = self.cursor.fetchone()['avg_cooking_time']
            
            # Most common categories
            self.cursor.execute("""
                SELECT jsonb_array_elements_text(category) as category, COUNT(*) as count
                FROM recipes
                GROUP BY category
                ORDER BY count DESC
                LIMIT 10
            """)
            stats['common_categories'] = self.cursor.fetchall()
            
            return stats
        except Exception as e:
            print(f"Error retrieving recipe statistics: {str(e)}")
            return {}
    
    def get_user_stats(self):
        """Get basic statistics about the users database"""
        try:
            stats = {}
            
            # Total number of users
            self.cursor.execute("SELECT COUNT(*) as total FROM users")
            stats['total_users'] = self.cursor.fetchone()['total']
            
            # Total number of reviews
            self.cursor.execute("SELECT COUNT(*) as total FROM reviews")
            stats['total_reviews'] = self.cursor.fetchone()['total']
            
            # Average rating given
            self.cursor.execute("SELECT AVG(rating) as avg_rating FROM reviews")
            stats['avg_rating'] = self.cursor.fetchone()['avg_rating']
            
            # Most active users
            self.cursor.execute("""
                SELECT u.username, COUNT(r.id) as review_count
                FROM users u
                JOIN reviews r ON u.user_id = r.user_id
                GROUP BY u.username
                ORDER BY review_count DESC
                LIMIT 10
            """)
            stats['most_active_users'] = self.cursor.fetchall()
            
            return stats
        except Exception as e:
            print(f"Error retrieving user statistics: {str(e)}")
            return {}

# Example usage
def main():
    # Database connection parameters
    DB_NAME = "recipe_chatbot"
    DB_USER = "postgres"  # Replace with your PostgreSQL username
    DB_PASSWORD = "1234"  # Replace with your PostgreSQL password
    DB_HOST = "localhost"
    DB_PORT = "5432"
    
    # Create and connect to the database
    db = RecipeDatabase(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    if db.connect():
        try:
            # Simple test queries
            print("\n--- Top 5 Rated Recipes ---")
            top_recipes = db.get_top_rated_recipes(5)
            for recipe in top_recipes:
                print(f"{recipe['title']} - Rating: {recipe['ratings']}")
            
            print("\n--- Quick Recipes (Under 30 mins) ---")
            quick_recipes = db.get_quick_recipes(30, 5)
            for recipe in quick_recipes:
                print(f"{recipe['title']} - Time: {recipe['total_mins']} mins")
            
            print("\n--- Search for 'Chicken' recipes ---")
            chicken_recipes = db.search_recipes_by_title('Chicken', 5)
            for recipe in chicken_recipes:
                print(f"{recipe['title']} - Rating: {recipe['ratings']}")
            
            print("\n--- Basic Recipe Stats ---")
            stats = db.get_recipe_stats()
            print(f"Total Recipes: {stats['total_recipes']}")
            print(f"Average Rating: {stats['avg_rating']:.2f}")
            print(f"Average Calories: {stats['avg_calories']:.2f}")
            print(f"Average Cooking Time: {stats['avg_cooking_time']:.2f} minutes")
            
        finally:
            db.disconnect()

if __name__ == "__main__":
    main()