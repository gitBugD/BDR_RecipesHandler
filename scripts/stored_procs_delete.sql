CREATE OR REPLACE PROCEDURE delete_creator(idcreator int)
LANGUAGE SQL
AS $$
	DELETE FROM creator WHERE  id = idcreator;
$$;

CREATE OR REPLACE PROCEDURE delete_tool(idtool int)
LANGUAGE SQL
AS $$
	DELETE FROM tool WHERE  id = idtool;
$$;

CREATE OR REPLACE PROCEDURE delete_allergen(idallergen int)
LANGUAGE SQL
AS $$
	DELETE FROM allergen WHERE  id = idallergen;
$$;

CREATE OR REPLACE PROCEDURE delete_ingredient(idingredient int)
LANGUAGE SQL
AS $$
	DELETE FROM ingredient WHERE  id = idingredient;
$$;

CREATE OR REPLACE PROCEDURE delete_recipe(idrecipe int)
LANGUAGE SQL
AS $$
	DELETE FROM recipe WHERE  id = idrecipe;
$$;

CREATE OR REPLACE PROCEDURE delete_step(idrecipe_step int, nbstep int)
LANGUAGE SQL
AS $$
	DELETE FROM step WHERE idrecipe = idrecipe_step AND nb = nbstep;
$$;

CREATE OR REPLACE PROCEDURE delete_all_ingredient_restriction(IN idingredient integer)
LANGUAGE sql
AS $$
	DELETE FROM ingredient_restriction WHERE ingredient_restriction.idingredient = idingredient;
$$;

CREATE OR REPLACE PROCEDURE delete_all_ingredient_season(IN idingredient integer)
 LANGUAGE sql
AS $$
	DELETE FROM ingredient_season WHERE ingredient_season.idingredient = idingredient;
$$;