import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import ast
import json
import re

def print_dataframe_info(df, name):
    """Print information about the DataFrame for debugging"""
    print(f"\nDataFrame: {name}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Shape: {df.shape}")
    print("First row:")
    print(df.iloc[0])
    print("\n")

def clean_numeric_value(value):
    """Convert values like '2k' to integers (2000)"""
    if isinstance(value, str):
        # Handle 'k' suffix (thousands)
        if value.lower().endswith('k'):
            try:
                return int(float(value[:-1]) * 1000)
            except ValueError:
                return 0
        # Handle other potential formats
        try:
            return int(value)
        except ValueError:
            try:
                return int(float(value))
            except ValueError:
                return 0
    return value

def clean_ingredient_list(ingredients_str):
    """Clean the string representation of the ingredients list for proper PostgreSQL storage"""
    try:
        # Parse the string as a Python list
        ingredients_list = ast.literal_eval(ingredients_str)
        # Convert to a proper JSON-compatible list
        return json.dumps(ingredients_list)
    except:
        # If parsing fails, return an empty list
        return json.dumps([])

def clean_category_list(categories_str):
    """Clean the string representation of the categories list for proper PostgreSQL storage"""
    try:
        # Parse the string as a Python list
        categories_list = ast.literal_eval(categories_str)
        # Convert to a proper JSON-compatible list
        return json.dumps(categories_list)
    except:
        # If parsing fails, return an empty list
        return json.dumps([])

def import_data_to_postgresql(db_name, db_user, db_password, db_host='localhost', db_port='5432'):
    """Import CSV data into PostgreSQL database"""
    
    # Connect to PostgreSQL server (to create a new database if needed)
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if database exists, create it if not
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    if not exists:
        print(f"Creating database: {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
    
    cursor.close()
    conn.close()
    
    # Connect to the target database
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    print("Creating tables...")
    
    # Recipe table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        recipe_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        calories INTEGER,
        total_mins INTEGER,
        ingredients JSONB,
        category JSONB,
        ratings FLOAT,
        reviews INTEGER
    )
    """)
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL
    )
    """)
    
    # Reviews table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        recipe_id INTEGER REFERENCES recipes(recipe_id),
        rating INTEGER CHECK (rating BETWEEN 1 AND 5),
        review TEXT,
        date DATE,
        UNIQUE(user_id, recipe_id)
    )
    """)
    
    # Load recipe data with explicit header handling
    print("Loading recipe data...")
    recipes_df = pd.read_csv('Data/recipes/all_recipes.csv')
    
    # Check and fix column names if needed
    if any(col.startswith('data/recipes/all_recipes.csv') for col in recipes_df.columns):
        # Fix column names by removing prefix
        recipes_df.columns = [col.replace('data/recipes/all_recipes.csv', '') for col in recipes_df.columns]
    
    # Debug information
    print_dataframe_info(recipes_df, "recipes_df")
    
    # Clean up recipe data
    # Ensure columns exist before processing
    if 'ingredients' in recipes_df.columns:
        recipes_df['ingredients'] = recipes_df['ingredients'].apply(clean_ingredient_list)
    else:
        print("Warning: 'ingredients' column not found in recipes CSV")
        recipes_df['ingredients'] = json.dumps([])
        
    if 'category' in recipes_df.columns:
        recipes_df['category'] = recipes_df['category'].apply(clean_category_list)
    else:
        print("Warning: 'category' column not found in recipes CSV")
        recipes_df['category'] = json.dumps([])
    
    # Remove duplicates - keep the first occurrence of each recipe_id
    recipes_df = recipes_df.drop_duplicates(subset=['recipe_id'])
    print(f"After removing duplicates, {len(recipes_df)} unique recipes remain.")
    
    # Insert recipe data
    print(f"Inserting {len(recipes_df)} recipes...")
    
    # Create a list to store the values for each row
    recipe_data = []
    
    # Dynamically get values from DataFrame based on column presence
    for _, row in recipes_df.iterrows():
        recipe_id = clean_numeric_value(row.get('recipe_id', 0))
        title = row.get('title', '')
        calories = clean_numeric_value(row.get('calories', 0))
        total_mins = clean_numeric_value(row.get('total_mins', 0))
        ingredients = row.get('ingredients', json.dumps([]))
        category = row.get('category', json.dumps([]))
        ratings = row.get('ratings', 0.0)
        reviews = clean_numeric_value(row.get('reviews', 0))
        
        recipe_data.append((
            recipe_id,
            title,
            calories,
            total_mins,
            ingredients,
            category,
            ratings,
            reviews
        ))
    
    # Process batch inserts to avoid duplicates
    batch_size = 100
    for i in range(0, len(recipe_data), batch_size):
        batch = recipe_data[i:i+batch_size]
        execute_values(
            cursor,
            """
            INSERT INTO recipes (recipe_id, title, calories, total_mins, ingredients, category, ratings, reviews)
            VALUES %s
            ON CONFLICT (recipe_id) DO UPDATE SET
                title = EXCLUDED.title,
                calories = EXCLUDED.calories,
                total_mins = EXCLUDED.total_mins,
                ingredients = EXCLUDED.ingredients,
                category = EXCLUDED.category,
                ratings = EXCLUDED.ratings,
                reviews = EXCLUDED.reviews
            """,
            batch
        )
    
    # Load users data
    print("Loading user data...")
    users_df = pd.read_csv('Data/users/all_users.csv')
    
    # Debug information
    print_dataframe_info(users_df, "users_df")
    
    # Extract unique users
    unique_users = users_df[['user_id', 'username']].drop_duplicates()
    
    # Insert user data
    print(f"Inserting {len(unique_users)} users...")
    user_data = [
        (clean_numeric_value(row['user_id']), row['username'])
        for _, row in unique_users.iterrows()
    ]
    
    # Process batch inserts for users
    batch_size = 100
    for i in range(0, len(user_data), batch_size):
        batch = user_data[i:i+batch_size]
        execute_values(
            cursor,
            """
            INSERT INTO users (user_id, username)
            VALUES %s
            ON CONFLICT (user_id) DO UPDATE SET
                username = EXCLUDED.username
            """,
            batch
        )
    
    # Get all valid recipe_ids from the recipes table
    valid_recipe_ids = set(recipes_df['recipe_id'].unique())
    
    # Filter the users_df to only include reviews for valid recipes
    original_review_count = len(users_df)
    users_df = users_df[users_df['recipe_id'].isin(valid_recipe_ids)]
    filtered_review_count = len(users_df)
    
    print(f"Filtered out {original_review_count - filtered_review_count} reviews with invalid recipe_ids.")
    print(f"Remaining reviews: {filtered_review_count}")
    
    # Insert review data
    print(f"Inserting {len(users_df)} reviews...")
    review_data = []
    
    # Remove duplicate reviews (same user_id and recipe_id)
    users_df = users_df.drop_duplicates(subset=['user_id', 'recipe_id'])
    print(f"After removing duplicates, {len(users_df)} unique reviews remain.")
    
    for _, row in users_df.iterrows():
        user_id = clean_numeric_value(row.get('user_id', 0))
        recipe_id = clean_numeric_value(row.get('recipe_id', 0))
        rating = clean_numeric_value(row.get('rating', 0))
        review = row.get('review', '')
        date_str = row.get('date', None)
        
        review_data.append((
            user_id,
            recipe_id,
            rating,
            review,
            date_str
        ))
    
    # Process batch inserts for reviews
    batch_size = 100
    for i in range(0, len(review_data), batch_size):
        batch = review_data[i:i+batch_size]
        execute_values(
            cursor,
            """
            INSERT INTO reviews (user_id, recipe_id, rating, review, date)
            VALUES %s
            ON CONFLICT (user_id, recipe_id) DO UPDATE SET
                rating = EXCLUDED.rating,
                review = EXCLUDED.review,
                date = EXCLUDED.date
            """,
            batch
        )
    
    # Create indexes for better performance
    print("Creating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_calories ON recipes(calories)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_recipe_id ON reviews(recipe_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id)")
    
    # Create a GIN index for JSONB ingredients for faster searching
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_ingredients ON recipes USING GIN (ingredients)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes USING GIN (category)")
    
    print("Database setup complete!")
    
    # Return connection and cursor for further operations
    return conn, cursor

def create_ingredients_table(conn, cursor):
    """Extract all unique ingredients and create a separate ingredients table"""
    print("Creating ingredients table...")
    
    # Create the table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        clean_name TEXT NOT NULL,
        common_unit TEXT
    )
    """)
    
    # Get all ingredients from recipes
    cursor.execute("SELECT recipe_id, ingredients FROM recipes")
    all_recipes = cursor.fetchall()
    
    # Extract and clean all ingredients
    all_ingredients = set()
    for recipe_id, ingredients_json in all_recipes:
        try:
            # Make sure ingredients_json is a string before parsing
            if isinstance(ingredients_json, str):
                ingredients = json.loads(ingredients_json)
            else:
                # If it's already a list, use it directly
                ingredients = ingredients_json
                
            for ingredient in ingredients:
                # Basic cleaning for duplicate detection
                clean_name = re.sub(r'^\d+\s*(\d/\d)*\s*', '', ingredient.lower())
                clean_name = re.sub(r'\([^)]*\)', '', clean_name)
                clean_name = clean_name.strip()
                
                # Add to the set of all ingredients
                all_ingredients.add((ingredient, clean_name))
        except Exception as e:
            print(f"Warning: Could not parse ingredients for recipe {recipe_id}: {str(e)}")
    
    # Insert unique ingredients
    print(f"Inserting {len(all_ingredients)} unique ingredients...")
    
    # Process batch inserts for ingredients
    ingredient_data = list(all_ingredients)
    batch_size = 100
    for i in range(0, len(ingredient_data), batch_size):
        batch = ingredient_data[i:i+batch_size]
        for ingredient, clean_name in batch:
            try:
                cursor.execute(
                    """
                    INSERT INTO ingredients (name, clean_name, common_unit)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                    """,
                    (ingredient, clean_name, None)
                )
            except Exception as e:
                print(f"Error inserting ingredient '{ingredient}': {str(e)}")
    
    # Create index
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ingredients_clean_name ON ingredients(clean_name)")
    
    print("Ingredients table created!")

def create_recipe_ingredients_table(conn, cursor):
    """Create a junction table linking recipes and ingredients"""
    print("Creating recipe_ingredients junction table...")
    
    # Create the table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        recipe_id INTEGER REFERENCES recipes(recipe_id),
        ingredient_id INTEGER REFERENCES ingredients(id),
        PRIMARY KEY (recipe_id, ingredient_id)
    )
    """)
    
    # Get all recipes and their ingredients
    cursor.execute("SELECT recipe_id, ingredients FROM recipes")
    all_recipes = cursor.fetchall()
    
    # For each recipe, find ingredient IDs and create links
    for recipe_id, ingredients_json in all_recipes:
        try:
            # Make sure ingredients_json is a string before parsing
            if isinstance(ingredients_json, str):
                ingredients = json.loads(ingredients_json)
            else:
                # If it's already a list, use it directly
                ingredients = ingredients_json
                
            for ingredient in ingredients:
                # Find the ingredient ID
                cursor.execute(
                    "SELECT id FROM ingredients WHERE name = %s",
                    (ingredient,)
                )
                result = cursor.fetchone()
                
                if result:
                    ingredient_id = result[0]
                    # Create the link
                    try:
                        cursor.execute(
                            """
                            INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
                            VALUES (%s, %s)
                            ON CONFLICT (recipe_id, ingredient_id) DO NOTHING
                            """,
                            (recipe_id, ingredient_id)
                        )
                    except Exception as e:
                        print(f"Error linking recipe {recipe_id} to ingredient {ingredient_id}: {str(e)}")
        except Exception as e:
            print(f"Warning: Could not parse ingredients for recipe {recipe_id}: {str(e)}")
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_recipe_id ON recipe_ingredients(recipe_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_ingredient_id ON recipe_ingredients(ingredient_id)")
    
    print("Recipe ingredients junction table created!")

def analyze_data_mismatch(recipes_df, users_df):
    """Analyze the mismatch between recipes and reviews data"""
    recipe_ids = set(recipes_df['recipe_id'].unique())
    review_recipe_ids = set(users_df['recipe_id'].unique())
    
    missing_recipes = review_recipe_ids - recipe_ids
    
    print(f"\nDATA MISMATCH ANALYSIS:")
    print(f"Total unique recipes in recipes_df: {len(recipe_ids)}")
    print(f"Total unique recipe_ids in reviews: {len(review_recipe_ids)}")
    print(f"Number of recipe_ids in reviews but not in recipes: {len(missing_recipes)}")
    
    if len(missing_recipes) > 0:
        print(f"Example missing recipe_ids: {list(missing_recipes)[:5]}")
    
    return missing_recipes

def main():
    # Database connection parameters
    DB_NAME = "recipe_chatbot"
    DB_USER = "postgres"  # Replace with your PostgreSQL username
    DB_PASSWORD = "1234"  # Replace with your PostgreSQL password
    DB_HOST = "localhost"
    DB_PORT = "5432"
    
    try:
        # Import data to PostgreSQL
        conn, cursor = import_data_to_postgresql(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
        
        # Create additional tables for better organization and querying
        create_ingredients_table(conn, cursor)
        create_recipe_ingredients_table(conn, cursor)
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("All data has been successfully imported into PostgreSQL!")
        print(f"Database: {DB_NAME}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check your CSV files and database connection parameters.")

if __name__ == "__main__":
    main()