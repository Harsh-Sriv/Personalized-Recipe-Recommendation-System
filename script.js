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

// Load recipes from JSON file
let allRecipes = [];

async function loadRecipes() {
    try {
        const response = await fetch('recipes.json');
        allRecipes = await response.json();
        console.log('Recipes loaded successfully:', allRecipes.length);
    } catch (error) {
        console.log('Using default recipes data');
        // If recipes.json fails to load, use the INGREDIENT_RECIPES data
        allRecipes = Object.values(INGREDIENT_RECIPES).flat();
        console.log('Loaded default recipes:', allRecipes.length);
    }
}

// DOM Elements
let recipeSearchInput;
let recipeResultsContainer;
let ingredientSearchInput;
let selectedIngredientsList;
let ingredientCheckboxes;

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize DOM elements
    recipeSearchInput = document.getElementById('recipeSearch');
    recipeResultsContainer = document.getElementById('recipeResults');
    ingredientSearchInput = document.getElementById('ingredientSearch');
    selectedIngredientsList = document.getElementById('selectedIngredientsList');
    ingredientCheckboxes = document.querySelectorAll('.ingredients-list input[type="checkbox"]');

    // Check if all required elements are found
    if (!recipeSearchInput || !recipeResultsContainer || !ingredientSearchInput || !selectedIngredientsList) {
        console.error('Some required DOM elements were not found. Please check the HTML structure.');
        return;
    }

    initializeIngredientHandlers();
    setupFormHandlers();
});

// Display recipes
function displayRecipes(recipes) {
    if (!recipes || recipes.length === 0) {
        recipeResultsContainer.innerHTML = '<p class="no-results">No recipes found matching your criteria. Try adjusting your preferences.</p>';
        return;
    }

    const recipesHTML = recipes.map(recipe => `
        <div class="recipe-card">
            <div class="recipe-image">
                <img src="${recipe.image_url || 'https://via.placeholder.com/150?text=No+Image'}" alt="${recipe.title}">
            </div>
            <div class="recipe-info">
                <h3>${recipe.title}</h3>
                <div class="recipe-meta">
                    ${recipe.calories ? `<span><i class="fas fa-fire"></i> ${recipe.calories} calories</span>` : ''}
                    ${recipe.total_mins ? `<span><i class="fas fa-clock"></i> ${recipe.total_mins} mins</span>` : ''}
                    ${recipe.ratings ? `<span><i class="fas fa-star"></i> ${recipe.ratings.toFixed(1)}</span>` : ''}
                </div>
                <div class="recipe-ingredients">
                    <strong>Ingredients:</strong>
                    <p>${recipe.ingredients.join(', ')}</p>
                </div>
                <button onclick="viewRecipeDetails('${recipe.recipe_id}')" class="view-recipe-btn">View Recipe</button>
            </div>
        </div>
    `).join('');

    recipeResultsContainer.innerHTML = `
        <h2>Recommended Recipes</h2>
        <div class="recipe-grid">
            ${recipesHTML}
        </div>
    `;
}

// Load settings when the page loads
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Page loaded, initializing...');
    await loadRecipes();
    loadSettings();
    setupEventListeners();
    initializeIngredientHandlers();
    setupFormHandlers();
    loadCommonIngredients();
    displayRecipeDetails();

    // Initial recipe search to show some results
    const initialRecipes = filterRecipes({
        ingredients: [],
        maxCalories: 1000,
        dietaryRestrictions: [],
        cookingTime: 60,
        difficultyLevel: 'any'
    });
    displayRecipeResults(initialRecipes);
});

// Setup event listeners for forms
function setupEventListeners() {
    // Recipe form submission
    const recipeForm = document.getElementById('recipeForm');
    if (recipeForm) {
        console.log('Setting up recipe form event listener');
        recipeForm.addEventListener('submit', handleFormSubmit);
    } else {
        console.error('Recipe form not found');
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

// Update the recipe search function to use real data
async function handleRecipeSearch(event) {
    event.preventDefault();

    const formData = {
        ingredients: getSelectedIngredients(),
        maxCalories: document.getElementById('maxCalories').value,
        dietaryRestrictions: Array.from(document.querySelectorAll('input[name="dietaryRestrictions"]:checked')).map(cb => cb.value),
        cookingTime: document.getElementById('cookingTime').value,
        difficultyLevel: document.getElementById('difficultyLevel').value
    };

    const filteredRecipes = filterRecipes(formData);
    displayRecipeResults(filteredRecipes);
}

function filterRecipes(filters) {
    console.log('Filtering recipes with:', filters);
    return allRecipes.filter(recipe => {
        // Check ingredients
        const hasIngredients = filters.ingredients.length === 0 ||
            filters.ingredients.some(ingredient =>
                recipe.ingredients.some(recipeIngredient =>
                    recipeIngredient.toLowerCase().includes(ingredient.toLowerCase())
                )
            );

        // Check calories
        const withinCalories = !filters.maxCalories || recipe.calories <= filters.maxCalories;

        // Check cooking time
        const withinTime = !filters.cookingTime || recipe.cookingTime <= filters.cookingTime;

        // Check dietary restrictions
        const matchesDietary = filters.dietaryRestrictions.length === 0 ||
            filters.dietaryRestrictions.every(restriction => {
                if (restriction === 'vegetarian') {
                    return !recipe.ingredients.some(ing =>
                        ['chicken', 'beef', 'pork', 'lamb', 'turkey', 'fish', 'seafood'].includes(ing.toLowerCase())
                    );
                } else if (restriction === 'vegan') {
                    return !recipe.ingredients.some(ing =>
                        ['chicken', 'beef', 'pork', 'lamb', 'turkey', 'fish', 'seafood', 'milk', 'cheese', 'butter', 'egg', 'yogurt'].includes(ing.toLowerCase())
                    );
                } else if (restriction === 'gluten-free') {
                    return !recipe.ingredients.some(ing =>
                        ['wheat', 'flour', 'bread', 'pasta', 'barley', 'rye'].includes(ing.toLowerCase())
                    );
                }
                return true;
            });

        const matches = hasIngredients && withinCalories && withinTime && matchesDietary;
        console.log('Recipe matches filters:', recipe.title, matches);
        return matches;
    });
}

function displayRecipeResults(recipes) {
    console.log('Displaying recipe results:', recipes);
    const resultsContainer = document.getElementById('recipeResults');
    if (!resultsContainer) {
        console.error('Recipe results container not found');
        return;
    }

    if (!recipes || recipes.length === 0) {
        console.log('No recipes to display');
        resultsContainer.innerHTML = `
            <div class="no-results">
                <p>No recipes found matching your criteria. Try adjusting your filters.</p>
            </div>
        `;
        return;
    }

    const recipesHTML = recipes.map(recipe => {
        console.log('Processing recipe:', recipe);
        return `
            <div class="recipe-card">
                <div class="recipe-image">
                    <img src="${recipe.image || 'https://via.placeholder.com/150?text=No+Image'}" alt="${recipe.title}">
                </div>
                <div class="recipe-info">
                    <h3>${recipe.title}</h3>
                    <p class="recipe-description">A delicious recipe made with ${recipe.ingredients.join(', ')}</p>
                    <div class="recipe-meta">
                        <span><i class="fas fa-clock"></i> ${recipe.cookingTime} mins</span>
                        <span><i class="fas fa-fire"></i> ${recipe.calories} calories</span>
                        <span><i class="fas fa-star"></i> ${recipe.rating}</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    resultsContainer.innerHTML = recipesHTML;
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

// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    console.log('Form submitted');

    const ingredients = Array.from(selectedIngredients);
    const maxCalories = document.getElementById('maxCalories').value;
    const dietaryRestrictions = Array.from(document.querySelectorAll('input[name="dietaryRestrictions"]:checked'))
        .map(checkbox => checkbox.value);
    const cookingTime = document.getElementById('cookingTime').value;
    const difficultyLevel = document.getElementById('difficultyLevel').value;

    console.log('Form data:', {
        ingredients,
        maxCalories,
        dietaryRestrictions,
        cookingTime,
        difficultyLevel
    });

    fetchRecipeRecommendations(
        ingredients,
        maxCalories,
        dietaryRestrictions,
        cookingTime,
        difficultyLevel
    );
}

// Function to view recipe details
async function viewRecipeDetails(recipeId) {
    try {
        // Fetch recipes from local JSON file
        const response = await fetch('recipes.json');
        const recipes = await response.json();

        // Find the recipe by ID
        const recipe = recipes.find(r => r.recipe_id === recipeId);

        if (!recipe) {
            console.error('Recipe not found');
            return;
        }

        // Store the recipe in sessionStorage for the details page
        sessionStorage.setItem('currentRecipe', JSON.stringify(recipe));

        // Navigate to the recipe details page
        window.location.href = 'recipe-details.html';
    } catch (error) {
        console.error('Error loading recipe details:', error);
    }
}

// Function to display recipe details on the details page
function displayRecipeDetails() {
    // Only run this on the recipe details page
    if (!window.location.pathname.includes('recipe-details.html')) {
        return;
    }

    const recipe = JSON.parse(sessionStorage.getItem('currentRecipe'));
    if (!recipe) {
        document.getElementById('recipeTitle').textContent = 'Recipe Not Found';
        return;
    }

    // Update the page title
    document.title = `${recipe.title} - Recipe Details`;

    // Update the header information
    document.getElementById('recipeTitle').textContent = recipe.title;
    document.getElementById('cookingTime').querySelector('span').textContent = `${recipe.total_mins} mins`;
    document.getElementById('calories').querySelector('span').textContent = `${recipe.calories} calories`;
    document.getElementById('rating').querySelector('span').textContent = recipe.ratings.toFixed(1);

    // Update the image
    const recipeImage = document.getElementById('recipeImage');
    recipeImage.src = recipe.image_url || 'https://via.placeholder.com/600x400?text=No+Image';
    recipeImage.alt = recipe.title;

    // Update categories
    const categoryTags = document.getElementById('categoryTags');
    categoryTags.innerHTML = recipe.category.map(cat =>
        `<span class="recipe-tag">${cat}</span>`
    ).join('');

    // Update ingredients
    const ingredientsList = document.getElementById('ingredientsList');
    ingredientsList.innerHTML = recipe.ingredients.map(ingredient =>
        `<li><i class="fas fa-check"></i> ${ingredient}</li>`
    ).join('');

    // Update instructions
    const instructionsList = document.getElementById('instructionsList');
    if (recipe.instructions) {
        instructionsList.innerHTML = recipe.instructions
            .split('\n')
            .filter(step => step.trim())
            .map(step => `<li>${step.trim()}</li>`)
            .join('');
    } else {
        instructionsList.innerHTML = '<li>No instructions available for this recipe.</li>';
    }
}

// Function to display error messages
function displayError(message) {
    const resultsContainer = document.getElementById('recipeResults');
    resultsContainer.innerHTML = `<p class="error-message">${message}</p>`;
}

async function fetchRecipes(filters) {
    try {
        // Build query string
        const params = new URLSearchParams();
        if (filters.ingredients) params.append('ingredients', filters.ingredients.join(','));
        if (filters.maxCalories) params.append('maxCalories', filters.maxCalories);
        if (filters.dietaryRestrictions.length > 0) {
            params.append('dietary', filters.dietaryRestrictions.join(','));
        }

        const response = await fetch(`http://localhost:3001/api/recipes?${params}`);
        if (!response.ok) throw new Error('Network response was not ok');

        return await response.json();
    } catch (error) {
        console.error('Error fetching recipes:', error);
        showError('Failed to load recipes. Please try again.');
        return [];
    }
}

// Fetch recipe recommendations
async function fetchRecipeRecommendations(
    ingredients,
    maxCalories,
    dietaryRestrictions,
    cookingTime,
    difficultyLevel
) {
    try {
        console.log('Search parameters:', {
            ingredients,
            maxCalories,
            dietaryRestrictions,
            cookingTime,
            difficultyLevel
        });

        // Fetch recipes from local JSON file
        const response = await fetch('recipes.json');
        const data = await response.json();
        console.log('Total recipes loaded:', data.length);

        // Filter recipes based on criteria
        const filteredRecipes = data.filter(recipe => {
            // Check if recipe has any of the selected ingredients
            const hasIngredients = ingredients.length === 0 ||
                ingredients.some(ingredient =>
                    recipe.ingredients.some(recipeIngredient =>
                        recipeIngredient.toLowerCase().includes(ingredient.toLowerCase())
                    )
                );

            // Check calories
            const withinCalories = !maxCalories || recipe.calories <= maxCalories;

            // Check cooking time
            const withinTime = !cookingTime || recipe.total_mins <= cookingTime;

            // Check dietary restrictions
            const matchesDietary = dietaryRestrictions.length === 0 ||
                dietaryRestrictions.every(restriction => {
                    if (restriction === 'vegetarian') {
                        return !recipe.ingredients.some(ing =>
                            ['beef', 'chicken', 'pork', 'lamb', 'turkey', 'fish', 'seafood'].includes(ing.toLowerCase())
                        );
                    } else if (restriction === 'vegan') {
                        return !recipe.ingredients.some(ing =>
                            ['beef', 'chicken', 'pork', 'lamb', 'turkey', 'fish', 'seafood', 'milk', 'cheese', 'butter', 'egg', 'yogurt'].includes(ing.toLowerCase())
                        );
                    } else if (restriction === 'gluten-free') {
                        return recipe.category.includes('Gluten-Free');
                    }
                    return true;
                });

            const matches = hasIngredients && withinCalories && withinTime && matchesDietary;
            if (matches) {
                console.log('Matching recipe:', recipe.title);
            }
            return matches;
        });

        console.log('Number of matching recipes:', filteredRecipes.length);

        // Sort recipes by number of matching ingredients
        const sortedRecipes = filteredRecipes.sort((a, b) => {
            const aMatches = a.ingredients.filter(ing =>
                ingredients.some(selectedIng =>
                    ing.toLowerCase().includes(selectedIng.toLowerCase())
                )
            ).length;

            const bMatches = b.ingredients.filter(ing =>
                ingredients.some(selectedIng =>
                    ing.toLowerCase().includes(selectedIng.toLowerCase())
                )
            ).length;

            return bMatches - aMatches;
        });

        // Add matching ingredients to each recipe
        const recipesWithMatches = sortedRecipes.map(recipe => ({
            ...recipe,
            matching_ingredients: recipe.ingredients.filter(ing =>
                ingredients.some(selectedIng =>
                    ing.toLowerCase().includes(selectedIng.toLowerCase())
                )
            )
        }));

        displayRecipes(recipesWithMatches);
    } catch (error) {
        console.error('Error fetching recipe recommendations:', error);
        recipeResultsContainer.innerHTML = '<p class="error">An error occurred while fetching recipe recommendations. Please try again.</p>';
    }
}