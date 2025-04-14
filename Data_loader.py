import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import ast
import json
import re
import traceback

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

def import_data_to_postgresql():
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="1234"  # Using the password from the main() function
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'recipe_recommendation'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE recipe_recommendation')
            print("Database 'recipe_recommendation' created successfully!")

        # Close the connection to postgres database before connecting to recipe_recommendation
        cursor.close()
        conn.close()

        # Connect to the recipe_recommendation database
        conn = psycopg2.connect(
            host="localhost",
            database="recipe_recommendation",
            user="postgres",
            password="1234"
        )
        cursor = conn.cursor()

        # Drop existing tables if they exist
        print("Dropping existing tables...")
        cursor.execute("""
            DROP TABLE IF EXISTS recipe_ingredients CASCADE;
            DROP TABLE IF EXISTS ingredients CASCADE;
            DROP TABLE IF EXISTS recipes CASCADE;
        """)
        print("Existing tables dropped successfully!")

        # Create new tables
        print("Creating new tables...")
        
        # Create recipes table with instructions field
        cursor.execute("""
            CREATE TABLE recipes (
                recipe_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                ingredients TEXT[],
                category TEXT[],
                ratings FLOAT,
                reviews INTEGER,
                calories INTEGER,
                total_mins INTEGER,
                image_url TEXT,
                instructions TEXT
            )
        """)
        
        # Create ingredients table
        cursor.execute("""
            CREATE TABLE ingredients (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                clean_name TEXT NOT NULL,
                common_unit TEXT
            )
        """)
        
        # Create recipe_ingredients junction table
        cursor.execute("""
            CREATE TABLE recipe_ingredients (
                recipe_id INTEGER REFERENCES recipes(recipe_id),
                ingredient_id INTEGER REFERENCES ingredients(id),
                PRIMARY KEY (recipe_id, ingredient_id)
            )
        """)
        
        print("Tables created successfully!")

        # Read and process the dataset
        print("Reading and processing dataset...")
        df = pd.read_csv('recipe_dataset_200_with_instructions.csv')
        
        # Convert numpy types to Python native types
        df['recipe_id'] = df['recipe_id'].astype(int)
        df['ratings'] = df['ratings'].astype(float)
        df['reviews'] = df['reviews'].astype(int)
        df['calories'] = df['calories'].astype(int)
        df['total_mins'] = df['total_mins'].astype(int)
        
        # Insert recipes
        print("Inserting recipes...")
        for _, row in df.iterrows():
            try:
                # Convert string representations of lists to actual lists
                ingredients_list = ast.literal_eval(str(row['ingredients']))
                category_list = ast.literal_eval(str(row['category']))
                
                cursor.execute("""
                    INSERT INTO recipes (recipe_id, title, ingredients, category, ratings, reviews, calories, total_mins, image_url, instructions)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(row['recipe_id']),
                    row['title'],
                    ingredients_list,
                    category_list,
                    float(row['ratings']),
                    int(row['reviews']),
                    int(row['calories']),
                    int(row['total_mins']),
                    row['image_url'],
                    row['instructions']
                ))
            except Exception as e:
                print(f"Error inserting recipe {row['recipe_id']}: {str(e)}")
                continue

        # Create indexes for better performance
        print("Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipe_title ON recipes(title);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipe_category ON recipes USING GIN(category);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipe_ingredients ON recipes USING GIN(ingredients);")
        
        # Commit the transaction
        conn.commit()
        print("Data imported successfully!")
        
        # Now create ingredients and recipe_ingredients tables
        create_ingredients_table(conn, cursor)
        create_recipe_ingredients_table(conn, cursor)
        
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        traceback.print_exc()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

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
    try:
        # Import data to PostgreSQL
        import_data_to_postgresql()
        print("All data has been successfully imported into PostgreSQL!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check your CSV files and database connection parameters.")

if __name__ == "__main__":
    main()