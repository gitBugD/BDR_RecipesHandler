CREATE OR REPLACE FUNCTION limit_nb_steps()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
	DECLARE nb_existing_steps int;
	DECLARE nb_next_step int;
	BEGIN
		SELECT COUNT(step.nb) INTO nb_existing_steps FROM step WHERE idrecipe = NEW.idrecipe GROUP BY idrecipe;
		SELECT MAX(step.nb) + 1 INTO nb_next_step FROM step WHERE idrecipe = NEW.idrecipe GROUP BY idrecipe;
		IF nb_existing_steps > 10 THEN RAISE EXCEPTION 'Too many steps for recipe' USING HINT = 'It is not possible to insert new steps';
		END IF;
		IF nb_next_step != NEW.nb THEN RAISE EXCEPTION 'Steps not in the right order %', nb_next_step USING HINT = 'Step numbers must follow numerical order';
		END IF;
		RETURN NEW;
	END;
$$;

DROP TRIGGER IF EXISTS check_nb_steps ON step;
CREATE TRIGGER check_nb_steps
BEFORE INSERT ON step
FOR EACH ROW
EXECUTE FUNCTION limit_nb_steps();