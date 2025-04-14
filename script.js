// Local Storage Keys
const STORAGE_KEYS = {
    DIETARY_PREFERENCES: 'dietaryPreferences',
    SEARCH_PREFERENCES: 'searchPreferences',
    COMMON_INGREDIENTS: 'commonIngredients',
    SAVED_RECIPES: 'savedRecipes'
};

// Recipe Images (for demo purposes)
const RECIPE_IMAGES = [
    'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1495521821757-a1efb6729352?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1473093226795-af9932fe5856?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1498837167922-ddd27525d352?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
    'https://images.unsplash.com/photo-1490645935967-10de6ba17061?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'
];

// Recipe Templates for more variety
const RECIPE_TEMPLATES = [
    {
        titlePrefix: "Delicious",
        titleSuffixes: ["Pasta", "Stir Fry", "Salad", "Soup", "Casserole", "Bowl", "Wrap", "Burger", "Pizza", "Tacos"],
        ingredients: ["olive oil", "garlic", "onion", "tomato", "bell pepper", "mushroom", "spinach", "chicken", "beef", "rice", "pasta", "cheese", "egg", "milk", "butter", "salt", "pepper", "oregano", "basil", "cumin", "paprika"],
        descriptions: [
            "A flavorful dish perfect for any occasion.",
            "A healthy and nutritious meal that's easy to prepare.",
            "A comforting classic with a modern twist.",
            "A quick and easy recipe that's full of flavor.",
            "A restaurant-quality dish you can make at home.",
            "A family-friendly meal that everyone will love.",
            "A gourmet creation that's surprisingly simple.",
            "A budget-friendly recipe that doesn't compromise on taste.",
            "A seasonal specialty that highlights fresh ingredients.",
            "An international dish with authentic flavors."
        ]
    }
];

// Ingredient Management
let selectedIngredients = new Set();

// Ingredient-specific recipes
const INGREDIENT_RECIPES = {
    'chicken': [
        {
            id: 'chicken1',
            title: 'Grilled Chicken Salad',
            ingredients: ['chicken breast', 'lettuce', 'tomatoes', 'cucumber', 'olive oil'],
            calories: 350,
            cookingTime: 25,
            difficulty: 'easy',
            image: RECIPE_IMAGES[0],
            rating: '4.5',
            time: 25,
            dietaryTags: ['High Protein']
        },
        {
            id: 'chicken2',
            title: 'Chicken Stir Fry',
            ingredients: ['chicken breast', 'broccoli', 'carrots', 'soy sauce', 'ginger'],
            calories: 320,
            cookingTime: 20,
            difficulty: 'easy',
            image: RECIPE_IMAGES[1],
            rating: '4.3',
            time: 20,
            dietaryTags: ['High Protein', 'Low Carb']
        }
    ],
    'beef': [
        {
            id: 'beef1',
            title: 'Beef and Broccoli',
            ingredients: ['beef strips', 'broccoli', 'soy sauce', 'garlic', 'ginger'],
            calories: 380,
            cookingTime: 25,
            difficulty: 'medium',
            image: RECIPE_IMAGES[2],
            rating: '4.6',
            time: 25,
            dietaryTags: ['High Protein']
        },
        {
            id: 'beef2',
            title: 'Beef Tacos',
            ingredients: ['ground beef', 'tortillas', 'lettuce', 'tomato', 'cheese'],
            calories: 420,
            cookingTime: 30,
            difficulty: 'easy',
            image: RECIPE_IMAGES[3],
            rating: '4.4',
            time: 30,
            dietaryTags: ['High Protein']
        }
    ],
    'fish': [
        {
            id: 'fish1',
            title: 'Grilled Salmon',
            ingredients: ['salmon fillet', 'lemon', 'dill', 'olive oil', 'asparagus'],
            calories: 340,
            cookingTime: 25,
            difficulty: 'medium',
            image: RECIPE_IMAGES[4],
            rating: '4.7',
            time: 25,
            dietaryTags: ['High Protein', 'Omega-3']
        },
        {
            id: 'fish2',
            title: 'Fish Tacos',
            ingredients: ['white fish', 'tortillas', 'cabbage slaw', 'lime', 'avocado'],
            calories: 360,
            cookingTime: 30,
            difficulty: 'medium',
            image: RECIPE_IMAGES[5],
            rating: '4.5',
            time: 30,
            dietaryTags: ['High Protein', 'Omega-3']
        }
    ],
    'vegetables': [
        {
            id: 'veg1',
            title: 'Vegetable Stir Fry',
            ingredients: ['broccoli', 'carrots', 'bell peppers', 'soy sauce', 'ginger'],
            calories: 280,
            cookingTime: 20,
            difficulty: 'easy',
            image: RECIPE_IMAGES[6],
            rating: '4.2',
            time: 20,
            dietaryTags: ['Vegetarian', 'Vegan']
        },
        {
            id: 'veg2',
            title: 'Roasted Vegetables',
            ingredients: ['zucchini', 'bell peppers', 'mushrooms', 'olive oil', 'herbs'],
            calories: 250,
            cookingTime: 35,
            difficulty: 'easy',
            image: RECIPE_IMAGES[7],
            rating: '4.4',
            time: 35,
            dietaryTags: ['Vegetarian', 'Vegan']
        }
    ],
    'pasta': [
        {
            id: 'pasta1',
            title: 'Pasta Primavera',
            ingredients: ['pasta', 'zucchini', 'cherry tomatoes', 'basil', 'parmesan'],
            calories: 420,
            cookingTime: 30,
            difficulty: 'medium',
            image: RECIPE_IMAGES[8],
            rating: '4.7',
            time: 30,
            dietaryTags: ['Vegetarian']
        },
        {
            id: 'pasta2',
            title: 'Creamy Mushroom Pasta',
            ingredients: ['pasta', 'mushrooms', 'cream', 'garlic', 'parmesan'],
            calories: 450,
            cookingTime: 25,
            difficulty: 'medium',
            image: RECIPE_IMAGES[9],
            rating: '4.6',
            time: 25,
            dietaryTags: ['Vegetarian']
        }
    ]
};

// Load settings when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, initializing...');
    loadSettings();
    setupEventListeners();
    initializeIngredientHandlers();
    setupFormHandlers();
    loadCommonIngredients();
    // Initial recipe search to show some results
    const initialRecipes = simulateRecipeSearchWithFilters(
        [], // no ingredients
        null, // no calorie limit
        [], // no dietary restrictions
        null, // no cooking time
        'any' // any difficulty
    );
    displayRecipes(initialRecipes);
});

// Setup event listeners for forms
function setupEventListeners() {
    // Recipe form submission
    const recipeForm = document.getElementById('recipeForm');
    if (recipeForm) {
        recipeForm.addEventListener('submit', handleRecipeSearch);
    }

    // Settings forms
    const dietaryForm = document.getElementById('dietaryPreferencesForm');
    const searchForm = document.getElementById('searchPreferencesForm');
    const ingredientsForm = document.getElementById('commonIngredientsForm');

    if (dietaryForm) {
        dietaryForm.addEventListener('change', () => saveSettings());
    }
    if (searchForm) {
        searchForm.addEventListener('change', () => saveSettings());
    }
    if (ingredientsForm) {
        ingredientsForm.addEventListener('change', () => saveSettings());
    }
}

// Load settings from local storage
function loadSettings() {
    // Load dietary preferences
    const dietaryPreferences = JSON.parse(localStorage.getItem(STORAGE_KEYS.DIETARY_PREFERENCES) || '{}');
    Object.entries(dietaryPreferences).forEach(([key, value]) => {
        const checkbox = document.querySelector(`input[name="${key}"]`);
        if (checkbox) checkbox.checked = value;
    });

    // Load search preferences
    const searchPreferences = JSON.parse(localStorage.getItem(STORAGE_KEYS.SEARCH_PREFERENCES) || '{}');
    Object.entries(searchPreferences).forEach(([key, value]) => {
        const input = document.getElementById(key);
        if (input) input.value = value;
    });

    // Load common ingredients
    const commonIngredients = localStorage.getItem(STORAGE_KEYS.COMMON_INGREDIENTS) || '';
    const ingredientsTextarea = document.getElementById('commonIngredients');
    if (ingredientsTextarea) ingredientsTextarea.value = commonIngredients;

    // Load saved recipes
    const savedRecipes = JSON.parse(localStorage.getItem(STORAGE_KEYS.SAVED_RECIPES) || '[]');
    displaySavedRecipes(savedRecipes);
}

// Save settings to local storage
function saveSettings() {
    // Save dietary preferences
    const dietaryPreferences = {};
    document.querySelectorAll('#dietaryPreferencesForm input[type="checkbox"]').forEach(checkbox => {
        dietaryPreferences[checkbox.name] = checkbox.checked;
    });
    localStorage.setItem(STORAGE_KEYS.DIETARY_PREFERENCES, JSON.stringify(dietaryPreferences));

    // Save search preferences
    const searchPreferences = {
        defaultMaxCalories: document.getElementById('defaultMaxCalories')?.value || '',
        defaultCookingTime: document.getElementById('defaultCookingTime')?.value || '',
        defaultDifficulty: document.getElementById('defaultDifficulty')?.value || 'any'
    };
    localStorage.setItem(STORAGE_KEYS.SEARCH_PREFERENCES, JSON.stringify(searchPreferences));

    // Save common ingredients
    const commonIngredients = document.getElementById('commonIngredients')?.value || '';
    localStorage.setItem(STORAGE_KEYS.COMMON_INGREDIENTS, commonIngredients);

    showNotification('Settings saved successfully!');
}

// Handle recipe search form submission
async function handleRecipeSearch(event) {
    if (event) {
        event.preventDefault();
    }
    
    const formData = {
        ingredients: document.getElementById('ingredients').value,
        maxCalories: document.getElementById('maxCalories').value,
        dietaryRestrictions: Array.from(document.getElementById('dietaryRestrictions').selectedOptions).map(option => option.value),
        cookingTime: document.getElementById('cookingTime').value,
        difficulty: document.getElementById('difficulty').value
    };

    try {
        // Here you would typically make an API call to your backend
        // For now, we'll simulate a response
        const recipes = await simulateRecipeSearch(formData);
        displayRecipes(recipes);
    } catch (error) {
        showNotification('Error searching for recipes: ' + error.message, 'error');
    }
}

// Simulate recipe search (replace with actual API call)
async function simulateRecipeSearch(formData) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Return mock data with images
    return [
        {
            id: 1,
            title: 'Grilled Chicken Salad',
            ingredients: ['chicken breast', 'lettuce', 'tomatoes', 'cucumber', 'olive oil'],
            calories: 350,
            cookingTime: 25,
            difficulty: 'easy',
            image: RECIPE_IMAGES[0],
            rating: '4.5',
            time: 25,
            dietaryTags: []
        },
        {
            id: 2,
            title: 'Vegetable Stir Fry',
            ingredients: ['broccoli', 'carrots', 'bell peppers', 'soy sauce', 'ginger'],
            calories: 280,
            cookingTime: 20,
            difficulty: 'easy',
            image: RECIPE_IMAGES[1],
            rating: '4.2',
            time: 20,
            dietaryTags: ['Vegetarian', 'Vegan']
        },
        {
            id: 3,
            title: 'Pasta Primavera',
            ingredients: ['pasta', 'zucchini', 'cherry tomatoes', 'basil', 'parmesan'],
            calories: 420,
            cookingTime: 30,
            difficulty: 'medium',
            image: RECIPE_IMAGES[2],
            rating: '4.7',
            time: 30,
            dietaryTags: ['Vegetarian']
        },
        {
            id: 4,
            title: 'Salmon with Asparagus',
            ingredients: ['salmon fillet', 'asparagus', 'lemon', 'dill', 'butter'],
            calories: 380,
            cookingTime: 25,
            difficulty: 'medium',
            image: RECIPE_IMAGES[3],
            rating: '4.8',
            time: 25,
            dietaryTags: ['Gluten-Free']
        },
        {
            id: 5,
            title: 'Chocolate Chip Cookies',
            ingredients: ['flour', 'butter', 'sugar', 'chocolate chips', 'vanilla extract'],
            calories: 150,
            cookingTime: 35,
            difficulty: 'easy',
            image: RECIPE_IMAGES[4],
            rating: '4.6',
            time: 35,
            dietaryTags: ['Vegetarian']
        }
    ];
}

// Display recipes in the results section
function displayRecipes(recipes) {
    const resultsContainer = document.getElementById('recipe-results');
    resultsContainer.innerHTML = '';

    if (recipes.length === 0) {
        resultsContainer.innerHTML = '<p class="no-results">No recipes found matching your criteria.</p>';
        return;
    }

    recipes.forEach(recipe => {
        const recipeCard = document.createElement('div');
        recipeCard.className = 'recipe-card';
        
        // Create recipe image
        const imageContainer = document.createElement('div');
        imageContainer.className = 'recipe-image';
        const img = document.createElement('img');
        img.src = recipe.image_url || 'https://via.placeholder.com/300x200?text=No+Image';
        img.alt = recipe.title;
        imageContainer.appendChild(img);
        
        // Create recipe content
        const content = document.createElement('div');
        content.className = 'recipe-content';
        
        // Recipe title and rating
        const header = document.createElement('div');
        header.className = 'recipe-header';
        header.innerHTML = `
            <h3>${recipe.title}</h3>
            <div class="recipe-rating">
                <span class="stars">${'★'.repeat(Math.round(recipe.ratings))}${'☆'.repeat(5-Math.round(recipe.ratings))}</span>
                <span class="rating-value">${recipe.ratings.toFixed(1)}</span>
                <span class="reviews">(${recipe.reviews} reviews)</span>
            </div>
        `;
        
        // Recipe details
        const details = document.createElement('div');
        details.className = 'recipe-details';
        details.innerHTML = `
            <div class="detail-item">
                <i class="fas fa-fire"></i>
                <span>${recipe.calories} calories</span>
            </div>
            <div class="detail-item">
                <i class="fas fa-clock"></i>
                <span>${recipe.total_mins} mins</span>
            </div>
            <div class="detail-item">
                <i class="fas fa-tags"></i>
                <span>${recipe.category.join(', ')}</span>
            </div>
        `;
        
        // Recipe ingredients
        const ingredients = document.createElement('div');
        ingredients.className = 'recipe-ingredients';
        ingredients.innerHTML = `
            <h4>Ingredients:</h4>
            <ul>
                ${recipe.ingredients.map(ing => `<li>${ing}</li>`).join('')}
            </ul>
        `;
        
        // Recipe instructions
        const instructions = document.createElement('div');
        instructions.className = 'recipe-instructions';
        instructions.innerHTML = `
            <h4>Instructions:</h4>
            <p>${recipe.instructions}</p>
        `;
        
        // Save recipe button
        const saveButton = document.createElement('button');
        saveButton.className = 'save-recipe-btn';
        saveButton.innerHTML = '<i class="fas fa-bookmark"></i> Save Recipe';
        saveButton.onclick = () => saveRecipe(recipe);
        
        // Assemble the recipe card
        content.appendChild(header);
        content.appendChild(details);
        content.appendChild(ingredients);
        content.appendChild(instructions);
        content.appendChild(saveButton);
        
        recipeCard.appendChild(imageContainer);
        recipeCard.appendChild(content);
        resultsContainer.appendChild(recipeCard);
    });
}

// Save a recipe to favorites
function saveRecipe(recipeTitle) {
    const savedRecipes = JSON.parse(localStorage.getItem(STORAGE_KEYS.SAVED_RECIPES) || '[]');
    if (!savedRecipes.includes(recipeTitle)) {
        savedRecipes.push(recipeTitle);
        localStorage.setItem(STORAGE_KEYS.SAVED_RECIPES, JSON.stringify(savedRecipes));
        displaySavedRecipes(savedRecipes);
        showNotification('Recipe saved successfully!');
    }
}

// Display saved recipes
function displaySavedRecipes(recipes) {
    const savedRecipesSection = document.getElementById('savedRecipes');
    if (!savedRecipesSection) return;

    savedRecipesSection.innerHTML = recipes.length ? `
        <div class="recipe-grid">
            ${recipes.map((recipe, index) => `
                <div class="recipe-card">
                    <div class="recipe-image" style="background-image: url('${RECIPE_IMAGES[index % RECIPE_IMAGES.length]}')"></div>
                    <div class="recipe-content">
                        <h3>${recipe}</h3>
                        <button onclick="removeSavedRecipe('${recipe}')" class="cta-button">Remove</button>
                    </div>
                </div>
            `).join('')}
        </div>
    ` : '<p>No saved recipes yet.</p>';
}

// Remove a saved recipe
function removeSavedRecipe(recipeTitle) {
    const savedRecipes = JSON.parse(localStorage.getItem(STORAGE_KEYS.SAVED_RECIPES) || '[]');
    const updatedRecipes = savedRecipes.filter(recipe => recipe !== recipeTitle);
    localStorage.setItem(STORAGE_KEYS.SAVED_RECIPES, JSON.stringify(updatedRecipes));
    displaySavedRecipes(updatedRecipes);
    showNotification('Recipe removed from saved recipes.');
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Function to initialize ingredient selection handlers
function initializeIngredientHandlers() {
    // Add event listeners to all ingredient checkboxes
    document.querySelectorAll('.ingredients-list input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', handleIngredientSelection);
    });

    // Add event listener to ingredient search
    const searchInput = document.getElementById('ingredientSearch');
    if (searchInput) {
        searchInput.addEventListener('input', handleIngredientSearch);
    }

    // Initialize selected ingredients from localStorage
    updateSelectedIngredientsList();
    updateIngredientsTextarea();
}

// Function to handle ingredient selection
function handleIngredientSelection(event) {
    const checkbox = event.target;
    const ingredient = checkbox.value;
    
    if (checkbox.checked) {
        addIngredient(ingredient);
    } else {
        removeIngredient(ingredient);
    }
    
    updateSelectedIngredientsList();
    updateIngredientsTextarea();
}

// Function to add an ingredient to the selection
function addIngredient(ingredient) {
    const selectedIngredients = getSelectedIngredients();
    if (!selectedIngredients.includes(ingredient)) {
        selectedIngredients.push(ingredient);
        saveSelectedIngredients(selectedIngredients);
    }
}

// Function to remove an ingredient from the selection
function removeIngredient(ingredient) {
    let selectedIngredients = getSelectedIngredients();
    selectedIngredients = selectedIngredients.filter(i => i !== ingredient);
    saveSelectedIngredients(selectedIngredients);
    
    // Uncheck the corresponding checkbox
    const checkbox = document.querySelector(`input[value="${ingredient}"]`);
    if (checkbox) {
        checkbox.checked = false;
    }
}

// Function to update the selected ingredients list in the sidebar
function updateSelectedIngredientsList() {
    const selectedIngredientsList = document.getElementById('selectedIngredientsList');
    const selectedIngredients = getSelectedIngredients();
    
    if (selectedIngredientsList) {
        selectedIngredientsList.innerHTML = selectedIngredients.map(ingredient => `
            <div class="selected-ingredient">
                <span>${ingredient}</span>
                <button onclick="removeIngredient('${ingredient}')" class="remove-ingredient">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
    }
}

// Function to update the ingredients textarea
function updateIngredientsTextarea() {
    const textarea = document.getElementById('selectedIngredients');
    const selectedIngredients = getSelectedIngredients();
    
    if (textarea) {
        textarea.value = selectedIngredients.join(', ');
    }
}

// Function to handle ingredient search
function handleIngredientSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    
    document.querySelectorAll('.ingredients-list label').forEach(label => {
        const ingredient = label.textContent.toLowerCase();
        if (ingredient.includes(searchTerm)) {
            label.style.display = 'block';
        } else {
            label.style.display = 'none';
        }
    });
}

// Function to get selected ingredients from localStorage
function getSelectedIngredients() {
    const stored = localStorage.getItem('selectedIngredients');
    return stored ? JSON.parse(stored) : [];
}

// Function to save selected ingredients to localStorage
function saveSelectedIngredients(ingredients) {
    localStorage.setItem('selectedIngredients', JSON.stringify(ingredients));
}

// Function to load common ingredients from the API
async function loadCommonIngredients() {
    try {
        const response = await fetch('/api/ingredients');
        const data = await response.json();
        
        if (data.success) {
            updateIngredientsList(data.ingredients);
        } else {
            console.error('Failed to load ingredients:', data.error);
        }
    } catch (error) {
        console.error('Error loading ingredients:', error);
    }
}

// Function to update the ingredients list with data from the API
function updateIngredientsList(ingredients) {
    // Group ingredients by category
    const categories = {
        'Vegetables': [],
        'Meat & Poultry': [],
        'Spices & Herbs': [],
        'Dairy & Eggs': [],
        'Grains & Pasta': []
    };
    
    ingredients.forEach(ingredient => {
        // Simple categorization logic - can be improved
        if (ingredient.includes('chicken') || ingredient.includes('beef') || ingredient.includes('pork')) {
            categories['Meat & Poultry'].push(ingredient);
        } else if (ingredient.includes('salt') || ingredient.includes('pepper') || ingredient.includes('herb')) {
            categories['Spices & Herbs'].push(ingredient);
        } else if (ingredient.includes('milk') || ingredient.includes('cheese') || ingredient.includes('egg')) {
            categories['Dairy & Eggs'].push(ingredient);
        } else if (ingredient.includes('rice') || ingredient.includes('pasta') || ingredient.includes('bread')) {
            categories['Grains & Pasta'].push(ingredient);
        } else {
            categories['Vegetables'].push(ingredient);
        }
    });
    
    // Update the DOM with categorized ingredients
    Object.entries(categories).forEach(([category, ingredients]) => {
        const categoryElement = document.querySelector(`.category h4:contains('${category}')`).closest('.category');
        if (categoryElement) {
            const ingredientsList = categoryElement.querySelector('.ingredients-list');
            if (ingredientsList) {
                ingredientsList.innerHTML = ingredients.map(ingredient => `
                    <label>
                        <input type="checkbox" value="${ingredient}"> ${ingredient}
                    </label>
                `).join('');
                
                // Re-add event listeners to new checkboxes
                ingredientsList.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                    checkbox.addEventListener('change', handleIngredientSelection);
                });
            }
        }
    });
}

// Function to set up form handlers
function setupFormHandlers() {
    const form = document.getElementById('recipeForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

// Function to handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = {
        ingredients: getSelectedIngredients(),
        maxCalories: document.getElementById('maxCalories').value,
        dietaryRestrictions: Array.from(document.querySelectorAll('input[name="dietaryRestrictions"]:checked')).map(cb => cb.value),
        cookingTime: document.getElementById('cookingTime').value,
        difficultyLevel: document.getElementById('difficultyLevel').value
    };
    
    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayRecipeResults(data.recipes);
        } else {
            console.error('Failed to get recommendations:', data.error);
            displayError('Failed to get recipe recommendations. Please try again.');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        displayError('An error occurred while getting recommendations. Please try again.');
    }
}

// Function to display recipe results
function displayRecipeResults(recipes) {
    const resultsContainer = document.getElementById('recipeResults');
    
    if (recipes.length === 0) {
        resultsContainer.innerHTML = '<p class="no-results">No recipes found matching your criteria. Try adjusting your preferences.</p>';
        return;
    }
    
    resultsContainer.innerHTML = recipes.map(recipe => `
        <div class="recipe-card" onclick="showRecipeDetails(${recipe.recipe_id})">
            <div class="recipe-image">
                <img src="${recipe.image_url || 'static/images/default-recipe.jpg'}" alt="${recipe.title}">
            </div>
            <div class="recipe-info">
                <h3>${recipe.title}</h3>
                <p class="recipe-description">${recipe.description || ''}</p>
                <div class="recipe-meta">
                    <span><i class="fas fa-fire"></i> ${recipe.calories} calories</span>
                    <span><i class="fas fa-clock"></i> ${recipe.total_mins} mins</span>
                    <span><i class="fas fa-star"></i> ${recipe.rating || 'N/A'}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// Function to show recipe details
async function showRecipeDetails(recipeId) {
    try {
        const response = await fetch(`/api/recipe/${recipeId}`);
        const data = await response.json();
        
        if (data.success) {
            const recipe = data.recipe;
            
            // Create and show modal with recipe details
            const modal = document.createElement('div');
            modal.className = 'recipe-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close-modal">&times;</span>
                    <h2>${recipe.title}</h2>
                    <div class="recipe-details">
                        <img src="${recipe.image_url || 'static/images/default-recipe.jpg'}" alt="${recipe.title}">
                        <div class="recipe-info">
                            <p><strong>Calories:</strong> ${recipe.calories}</p>
                            <p><strong>Cooking Time:</strong> ${recipe.total_mins} minutes</p>
                            <p><strong>Difficulty:</strong> ${recipe.difficulty}</p>
                            <p><strong>Rating:</strong> ${recipe.rating || 'N/A'}</p>
                        </div>
                        <div class="recipe-ingredients">
                            <h3>Ingredients</h3>
                            <ul>
                                ${recipe.ingredients.map(ing => `<li>${ing}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="recipe-instructions">
                            <h3>Instructions</h3>
                            <ol>
                                ${recipe.instructions.map(step => `<li>${step}</li>`).join('')}
                            </ol>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Add event listener to close modal
            modal.querySelector('.close-modal').addEventListener('click', () => {
                modal.remove();
            });
        } else {
            console.error('Failed to get recipe details:', data.error);
            displayError('Failed to load recipe details. Please try again.');
        }
    } catch (error) {
        console.error('Error getting recipe details:', error);
        displayError('An error occurred while loading recipe details. Please try again.');
    }
}

// Function to display error messages
function displayError(message) {
    const resultsContainer = document.getElementById('recipeResults');
    resultsContainer.innerHTML = `<p class="error-message">${message}</p>`;
} 