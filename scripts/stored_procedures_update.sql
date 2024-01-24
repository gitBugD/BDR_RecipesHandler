CREATE OR REPLACE PROCEDURE update_creator(idcreator int, namecreator varchar(50))
LANGUAGE SQL
AS $$
	UPDATE creator SET name = namecreator WHERE id = idcreator;
$$;

CREATE OR REPLACE PROCEDURE update_allergen(idallergen int, nameallergen varchar(50))
LANGUAGE SQL
AS $$
	UPDATE allergen SET name = nameallergen WHERE id = idallergen;
$$;

CREATE OR REPLACE PROCEDURE update_tool(idtool int, nametool varchar(50))
LANGUAGE SQL
AS $$
	UPDATE tool SET name = nametool WHERE id = idtool;
$$;

CREATE OR REPLACE PROCEDURE update_ingredient(idingredient int, nameingredient varchar(50), new_idallergen int = 0)
LANGUAGE plpgsql
AS $$
	BEGIN 
		IF new_idallergen = 0
	THEN
		UPDATE ingredient SET name = nameingredient, idallergen = NULL WHERE id = idingredient;
	ELSE	
		UPDATE ingredient SET name = nameingredient, idallergen = new_idallergen WHERE id = idingredient;
	END IF;
	END 
$$;
