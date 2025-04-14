// API base URL
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
let recipeSearchInput;
let recipeResultsContainer;
let ingredientSearchInput;
let selectedIngredientsList;
let ingredientCheckboxes;

// Selected ingredients set
let selectedIngredients = new Set();

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
    
    // Load common ingredients from API
    loadCommonIngredients();
});

// Load common ingredients from API
async function loadCommonIngredients() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/ingredients`);
        const data = await response.json();
        
        if (data.success && data.ingredients) {
            // Populate ingredient checkboxes with common ingredients
            populateIngredientCheckboxes(data.ingredients);
        } else {
            console.error('Failed to load common ingredients:', data.error);
        }
    } catch (error) {
        console.error('Error loading common ingredients:', error);
    }
}

// Populate ingredient checkboxes with common ingredients
function populateIngredientCheckboxes(ingredients) {
    const categoriesContainer = document.querySelector('.ingredient-categories');
    categoriesContainer.innerHTML = ''; // Clear existing categories

    // Group ingredients by first letter
    const groupedIngredients = {};
    ingredients.forEach(ingredient => {
        const firstLetter = ingredient.charAt(0).toUpperCase();
        if (!groupedIngredients[firstLetter]) {
            groupedIngredients[firstLetter] = [];
        }
        groupedIngredients[firstLetter].push(ingredient);
    });

    // Create category sections
    Object.keys(groupedIngredients).sort().forEach(letter => {
        const category = document.createElement('div');
        category.className = 'category';
        
        const categoryTitle = document.createElement('h4');
        categoryTitle.textContent = letter;
        
        const ingredientsList = document.createElement('div');
        ingredientsList.className = 'ingredients-list';
        ingredientsList.setAttribute('data-category', letter.toLowerCase());
        
        groupedIngredients[letter].forEach(ingredient => {
            const label = document.createElement('label');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = ingredient;
            checkbox.addEventListener('change', handleIngredientSelection);
            
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(` ${ingredient}`));
            ingredientsList.appendChild(label);
        });
        
        category.appendChild(categoryTitle);
        category.appendChild(ingredientsList);
        categoriesContainer.appendChild(category);
    });
}

// Initialize ingredient handlers
function initializeIngredientHandlers() {
    // Add event listener for ingredient search
    ingredientSearchInput.addEventListener('input', handleIngredientSearch);
}

// Handle ingredient selection
function handleIngredientSelection(event) {
    const checkbox = event.target;
    const ingredient = checkbox.value;
    
    if (checkbox.checked) {
        selectedIngredients.add(ingredient);
    } else {
        selectedIngredients.delete(ingredient);
    }
    
    updateSelectedIngredientsList();
    updateIngredientsTextarea();
}

// Update selected ingredients list
function updateSelectedIngredientsList() {
    const textarea = document.getElementById('selectedIngredients');
    if (textarea) {
        textarea.value = Array.from(selectedIngredients).join(', ');
    }
}

// Update ingredients textarea
function updateIngredientsTextarea() {
    const textarea = document.getElementById('selectedIngredients');
    if (textarea) {
        textarea.value = Array.from(selectedIngredients).join(', ');
    }
}

// Remove ingredient from selection
function removeIngredient(ingredient) {
    selectedIngredients.delete(ingredient);
    updateSelectedIngredientsList();
    updateIngredientsTextarea();
    
    // Uncheck the corresponding checkbox
    const checkbox = document.querySelector(`input[value="${ingredient}"]`);
    if (checkbox) {
        checkbox.checked = false;
    }
}

// Handle ingredient search
function handleIngredientSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    const categories = document.querySelectorAll('.category');
    
    categories.forEach(category => {
        const ingredients = category.querySelectorAll('label');
        let hasVisibleIngredients = false;
        
        ingredients.forEach(ingredient => {
            const text = ingredient.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                ingredient.style.display = '';
                hasVisibleIngredients = true;
            } else {
                ingredient.style.display = 'none';
            }
        });
        
        category.style.display = hasVisibleIngredients ? '' : 'none';
    });
}

// Setup form handlers
function setupFormHandlers() {
    const form = document.getElementById('recipeForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    
    const ingredients = Array.from(selectedIngredients);
    const maxCalories = document.getElementById('maxCalories').value;
    const dietaryRestrictions = Array.from(document.querySelectorAll('input[name="dietaryRestrictions"]:checked'))
        .map(checkbox => checkbox.value);
    const cookingTime = document.getElementById('cookingTime').value;
    const difficultyLevel = document.getElementById('difficultyLevel').value;
    
    fetchRecipeRecommendations(
        ingredients,
        maxCalories,
        dietaryRestrictions,
        cookingTime,
        difficultyLevel
    );
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
        const response = await fetch(`${API_BASE_URL}/api/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ingredients,
                maxCalories: parseInt(maxCalories),
                dietaryRestrictions,
                cookingTime: parseInt(cookingTime),
                difficultyLevel
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.recipes) {
            displayRecipes(data.recipes);
        } else {
            console.error('Failed to get recipe recommendations:', data.error);
            recipeResultsContainer.innerHTML = '<p class="error">Failed to get recipe recommendations. Please try again.</p>';
        }
    } catch (error) {
        console.error('Error fetching recipe recommendations:', error);
        recipeResultsContainer.innerHTML = '<p class="error">An error occurred while fetching recipe recommendations. Please try again.</p>';
    }
}

// Display recipes
function displayRecipes(recipes) {
    if (!recipes || recipes.length === 0) {
        recipeResultsContainer.innerHTML = '<p>No recipes found matching your criteria. Try adjusting your preferences.</p>';
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
                    ${recipe.rating ? `<span><i class="fas fa-star"></i> ${recipe.rating.toFixed(1)}</span>` : ''}
                </div>
                <div class="recipe-ingredients">
                    <strong>Matching Ingredients:</strong>
                    <p>${recipe.matching_ingredients.join(', ')}</p>
                </div>
                <button onclick="viewRecipeDetails(${recipe.recipe_id})" class="view-recipe-btn">View Recipe</button>
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

// View recipe details
async function viewRecipeDetails(recipeId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/recipe/${recipeId}`);
        const data = await response.json();
        
        if (data.success && data.recipe) {
            const recipe = data.recipe;
            const modal = document.createElement('div');
            modal.className = 'recipe-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close-modal">&times;</span>
                    <div class="recipe-details">
                        <h2>${recipe.title}</h2>
                        <div class="recipe-meta">
                            ${recipe.calories ? `<span><i class="fas fa-fire"></i> ${recipe.calories} calories</span>` : ''}
                            ${recipe.total_mins ? `<span><i class="fas fa-clock"></i> ${recipe.total_mins} mins</span>` : ''}
                            ${recipe.rating ? `<span><i class="fas fa-star"></i> ${recipe.rating.toFixed(1)}</span>` : ''}
                        </div>
                        <div class="recipe-image">
                            <img src="${recipe.image_url || 'https://via.placeholder.com/300?text=No+Image'}" alt="${recipe.title}">
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
            
            // Close modal when clicking the close button or outside the modal
            const closeBtn = modal.querySelector('.close-modal');
            closeBtn.onclick = () => modal.remove();
            window.onclick = (event) => {
                if (event.target === modal) {
                    modal.remove();
                }
            };
        } else {
            console.error('Failed to get recipe details:', data.error);
        }
    } catch (error) {
        console.error('Error fetching recipe details:', error);
    }
} 