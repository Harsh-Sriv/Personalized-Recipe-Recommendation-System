const express = require('express');
const cors = require('cors');
const app = express();
const recipes = require('./recipes.json');

app.use(cors());

// Search endpoint
app.get('/api/recipes', (req, res) => {
    const { ingredients, maxCalories, dietary } = req.query;

    let results = recipes;

    // Filter by ingredients
    if (ingredients) {
        const searchIngredients = ingredients.toLowerCase().split(',');
        results = results.filter(recipe =>
            searchIngredients.some(ing =>
                recipe.ingredients.some(recipeIng =>
                    recipeIng.toLowerCase().includes(ing)
                )
            )
        );
    }

    // Filter by calories
    if (maxCalories) {
        results = results.filter(recipe => recipe.calories <= maxCalories);
    }

    // Filter by dietary
    if (dietary) {
        const restrictions = dietary.toLowerCase().split(',');
        results = results.filter(recipe => {
            return restrictions.every(restriction => {
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
        });
    }

    res.json(results);
});

app.listen(3001, () => {
    console.log('API running on http://localhost:3001');
});