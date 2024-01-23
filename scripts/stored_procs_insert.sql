CREATE OR REPLACE PROCEDURE insert_creator(name varchar(50))
LANGUAGE SQL
AS $$
	INSERT INTO creator (name) VALUES (name);
$$;

CREATE OR REPLACE PROCEDURE insert_tool(name varchar(50))
LANGUAGE SQL
AS $$
	INSERT INTO tool (name) VALUES (name);
$$;

CREATE OR REPLACE PROCEDURE insert_allergen(name varchar(50))
LANGUAGE SQL
AS $$
	INSERT INTO allergen (name) VALUES (name);
$$;


CREATE OR REPLACE FUNCTION insert_ingredient(name varchar(50), idallergen int = 0)
RETURNS int
LANGUAGE plpgsql
AS $$
	DECLARE returnid integer;
	BEGIN 
		IF idallergen = 0
	THEN
		INSERT INTO ingredient (name) VALUES (name) RETURNING ingredient.id INTO returnid;
	ELSE
		INSERT INTO ingredient (name, idallergen) VALUES (name, idallergen) RETURNING ingredient.id INTO returnid;
	END IF;
	RETURN returnid;
	END 
$$;

CREATE OR REPLACE PROCEDURE insert_ingredient_season(idingredient int, nameseason SeasonEnum)
LANGUAGE SQL
AS $$
	INSERT INTO ingredient_season (idingredient,nameseason) VALUES (idingredient,nameseason);
$$;

CREATE OR REPLACE PROCEDURE insert_ingredient_restriction(idingredient int, namerestriction RestrictionEnum)
LANGUAGE SQL
AS $$
	INSERT INTO ingredient_restriction (idingredient,namerestriction) VALUES (idingredient,namerestriction);
$$;

CREATE OR REPLACE FUNCTION insert_recipe(name varchar(50), description text, nbpeople int, difficulty int, cost int, idcreator int)
RETURNS int
LANGUAGE plpgsql
AS $$
	DECLARE returnid integer;
	BEGIN
		INSERT INTO recipe (name, description, nbpeople, difficulty, cost, idcreator) 
		VALUES (name, description, nbpeople, difficulty, cost, idcreator) RETURNING recipe.id INTO returnid;
		RETURN returnid;
	END
$$;

CREATE OR REPLACE PROCEDURE insert_recipe_coursetype(idrecipe int, namecoursetype CourseTypeEnum)
LANGUAGE SQL
AS $$
	INSERT INTO recipe_coursetype (idrecipe,namecoursetype) VALUES (idrecipe,namecoursetype);
$$;

CREATE OR REPLACE PROCEDURE insert_step(idrecipe int, nb int, instructions TEXT, preptime int, cookingtime int = 0)
LANGUAGE SQL
AS $$
	INSERT INTO step (idrecipe, nb, instructions, preptime, cookingtime) 
	VALUES (idrecipe, nb, instructions, preptime, cookingtime);
$$;

CREATE OR REPLACE PROCEDURE insert_step_tool(idrecipe int, nbstep int, idtool int)
LANGUAGE SQL
AS $$
	INSERT INTO step_tool (idrecipe, nbstep, idtool) VALUES (idrecipe, nbstep, idtool);
$$;

CREATE OR REPLACE PROCEDURE insert_step_ingredient(idrecipe int, nbstep int, idingredient int, unit UnitEnum, quantity NUMERIC(5,2))
LANGUAGE SQL
AS $$
	INSERT INTO step_ingredient (idrecipe, nbstep, idingredient, unit, quantity) VALUES (idrecipe, nbstep, idingredient, unit, quantity);
$$;

