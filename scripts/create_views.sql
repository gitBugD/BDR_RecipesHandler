CREATE OR REPLACE VIEW home_select AS
SELECT DISTINCT recipe.id AS idrecipe, recipe.name AS recipe, recipe.description, recipe.difficulty, recipe.cost,
recipe_coursetype.namecoursetype AS coursetype, step.nb, step.instructions, step.preptime, step.cookingtime,
ingredient.id AS idingredient, ingredient.name AS ingredient, allergen.name AS allergen, ingredient_season.nameseason AS season, 
ingredient_restriction.namerestriction AS restriction, tool.name AS tool
    FROM recipe
    LEFT JOIN recipe_coursetype ON recipe.id = recipe_coursetype.idrecipe
    LEFT JOIN step ON recipe.id = step.idrecipe
    LEFT JOIN step_ingredient ON step_ingredient.idrecipe = step.idrecipe AND step_ingredient.nbstep = step.nb
    LEFT JOIN ingredient ON ingredient.id = step_ingredient.idingredient
    LEFT JOIN allergen ON ingredient.idallergen = allergen.id
    LEFT JOIN ingredient_season ON ingredient_season.idingredient = ingredient.id
    LEFT JOIN ingredient_restriction ON ingredient_restriction.idingredient = ingredient.id
    LEFT JOIN step_tool ON step_tool.idrecipe = step.idrecipe AND step_tool.nbstep = step.nb
    LEFT JOIN tool ON step_tool.idtool = tool.id
    ORDER BY recipe.name;
   
CREATE OR REPLACE VIEW recipe_steps AS
SELECT DISTINCT step.idrecipe, step.nb, step.instructions, step.preptime, step.cookingtime FROM step;

CREATE OR REPLACE VIEW creators AS 
SELECT id, name FROM creator ORDER BY name;

CREATE OR REPLACE VIEW allergens AS 
SELECT id, name FROM allergen ORDER BY name;

CREATE OR REPLACE VIEW ingredients AS 
SELECT id, name FROM ingredient ORDER BY name;

CREATE OR REPLACE VIEW tools AS 
SELECT id, name FROM tool ORDER BY name;

CREATE OR REPLACE VIEW min_recipe_time AS
	WITH total_time AS (SELECT SUM(step.preptime + step.cookingtime) AS total
    FROM recipe 
    LEFT JOIN step ON recipe.id = step.idrecipe
    GROUP BY recipe.id)
    SELECT * FROM total_time GROUP BY total_time.total HAVING total <= ALL(SELECT total FROM total_time);
   
CREATE OR REPLACE VIEW max_recipe_time AS
	WITH total_time AS (SELECT SUM(COALESCE(step.preptime, 0) + COALESCE(step.cookingtime, 0)) AS total
    FROM recipe
    LEFT JOIN step ON recipe.id = step.idrecipe
    GROUP BY recipe.id)
    SELECT * FROM total_time GROUP BY total_time.total HAVING total >= ALL(SELECT total FROM total_time);

CREATE OR REPLACE VIEW single_recipe AS
SELECT DISTINCT recipe.id, recipe.name, recipe.description, recipe.nbpeople, 
recipe.difficulty, recipe.cost, creator.id as creatorid, creator.name as creator
    FROM recipe LEFT JOIN creator ON recipe.idcreator = creator.id
    LEFT JOIN recipe_coursetype ON recipe.id = recipe_coursetype.idrecipe;

CREATE OR REPLACE VIEW recipe_ingredients AS
SELECT DISTINCT step.idrecipe, ingredient.id, ingredient.name,
    step_ingredient.quantity, step_ingredient.unit FROM step
 	LEFT JOIN step_ingredient ON step.idrecipe = step_ingredient.idrecipe AND step.nb = step_ingredient.nbstep
 	LEFT JOIN ingredient ON ingredient.id = step_ingredient.idingredient
	WHERE ingredient.id IS NOT NULL;

CREATE OR REPLACE VIEW recipe_allergens AS
SELECT DISTINCT step.idrecipe, allergen.id, allergen.name FROM step
 	LEFT JOIN step_ingredient ON step.idrecipe = step_ingredient.idrecipe AND step.nb = step_ingredient.nbstep
 	LEFT JOIN ingredient ON ingredient.id = step_ingredient.idingredient
 	LEFT JOIN allergen ON allergen.id = ingredient.idallergen
	WHERE allergen.id IS NOT NULL;

CREATE OR REPLACE VIEW recipe_tools AS
SELECT DISTINCT step.idrecipe, tool.id, tool.name FROM step
 	LEFT JOIN step_tool ON step.idrecipe = step_tool.idrecipe AND step.nb = step_tool.nbstep
 	LEFT JOIN tool ON tool.id = step_tool.idtool
	WHERE tool.id IS NOT NULL;

CREATE OR REPLACE VIEW ingredients_details
AS SELECT ingredient.id AS idingredient,
    ingredient.name AS ingredient,
    ingredient.idallergen,
    allergen.name AS allergen,
    ingredient_restriction.namerestriction,
    ingredient_season.nameseason
   FROM ingredient
     LEFT JOIN allergen ON allergen.id = ingredient.idallergen
     LEFT JOIN ingredient_restriction ON ingredient_restriction.idingredient = ingredient.id
     LEFT JOIN ingredient_season ON ingredient_season.idingredient = ingredient.id;