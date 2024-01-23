WITH allergen_nuts AS (
INSERT
	INTO
	public.allergen ("name")
VALUES
	 ('nuts') RETURNING id
),
allergen_eggs AS(
INSERT
	INTO
	public.allergen ("name")
VALUES
	 ('eggs') RETURNING id
),
allergen_lactose AS(
INSERT
	INTO
	public.allergen ("name")
VALUES
	 ('lactose') RETURNING id
),
allergen_fish AS(
INSERT
	INTO
	public.allergen ("name")
VALUES
	 ('fish') RETURNING id
),
other_allergens AS(
INSERT
	INTO
	public.allergen ("name")
VALUES
	 ('peanuts'),
	 ('soy'),
	 ('gluten'),
	 ('crustaceans'),
	 ('celery'),
	 ('mustard'),
	 ('sesame'),
	 ('lupins'),
	 ('clams'),
	 ('kiwi'),
	 ('apple')
),
creator_remy AS(
INSERT
	INTO
	public.creator ("name")
VALUES
	 ('Remy le chef') RETURNING id
),
other_creators AS(
INSERT
	INTO
	public.creator ("name")
VALUES
	 ('Benedetta'),
	 ('Pina'),
	 ('Maxime')
),
tool_grill_pan AS(
INSERT
	INTO
		public.tool("name")
	VALUES ('grill pan') RETURNING id
),
tool_oven AS(
INSERT
	INTO
		public.tool("name")
	VALUES ('oven') RETURNING id
),
tool_blender AS(
INSERT
	INTO
		public.tool("name")
	VALUES ('blender') RETURNING id
),
tool_baking_dish AS(
INSERT
	INTO
		public.tool("name")
	VALUES ('baking dish') RETURNING id
),
ingredient_eggplant AS(
INSERT
	INTO
		public.ingredient("name")
	VALUES ('eggplant')
RETURNING id
),
ingredient_mozzarella AS(
INSERT
	INTO
		public.ingredient("name",
		idAllergen)
	VALUES ('mozzarella',
	(
	SELECT
		id
	FROM
		allergen_lactose))
RETURNING id
),
ingredient_parmigiano AS(
INSERT
	INTO
		public.ingredient("name",
		idAllergen)
	VALUES ('parmigiano',
	(
	SELECT
		id
	FROM
		allergen_lactose))
RETURNING id
),
ingredient_tomato_sauce AS(
INSERT
	INTO
		public.ingredient("name")
	VALUES ('tomato sauce')
RETURNING id
),
ingredient_nuts AS(
INSERT
	INTO
		public.ingredient("name",
		idAllergen)
	VALUES ('nuts',
	(
	SELECT
		id
	FROM
		allergen_nuts))
RETURNING id
),
ingredient_bananas AS(
INSERT
	INTO
		public.ingredient("name")
	VALUES ('bananas')
RETURNING id
),
ingredient_oats AS(
INSERT
	INTO
		public.ingredient("name")
	VALUES ('oats')
RETURNING id
),
ingredient_seed_oil AS(
INSERT
	INTO
		public.ingredient("name")
	VALUES ('seed oil')
RETURNING id
),
ingredient_sunflower_seeds AS(
INSERT
	INTO
		public.ingredient("name")
	VALUES ('sunflower seeds')
RETURNING id
),
ingredient_boiled_chestnuts AS(
INSERT
	INTO
		public.ingredient("name")
	VALUES ('boiled chestnuts')
RETURNING id
),
ingredient_sweet_potatoes AS(
INSERT
	INTO
		public.ingredient("name")
	VALUES ('sweet potatoes')
RETURNING id
),
ingredient_fish AS(
INSERT
	INTO
		public.ingredient("name",
		idAllergen)
	VALUES ('fish',
	(
	SELECT
		id
	FROM
		allergen_fish))
RETURNING id
),
ingredient_eggs AS(
INSERT
	INTO
		public.ingredient("name",
		idAllergen)
	VALUES ('eggs',
	(
	SELECT
		id
	FROM
		allergen_eggs))
RETURNING id
),
ingredients_restrictions AS(
INSERT
	INTO
	public.ingredient_restriction (idingredient,
	namerestriction)
VALUES
	 ((
SELECT
	id
FROM
	ingredient_fish),
'fish free'),
	 ((
SELECT
	id
FROM
	ingredient_mozzarella),
'vegan'),
	 ((
SELECT
	id
FROM
	ingredient_parmigiano),
'vegan'),
	 ((
SELECT
	id
FROM
	ingredient_fish),
'vegetarian'),
	 ((
SELECT
	id
FROM
	ingredient_eggs),
'vegan'),
	 ((
SELECT
	id
FROM
	ingredient_fish),
'vegan')), ingredients_seasons AS(
INSERT
	INTO
	public.ingredient_season (idingredient,
	nameseason)
VALUES
	 ((
SELECT
	id
FROM
	ingredient_fish),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_fish),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_fish),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_fish),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_mozzarella),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_mozzarella),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_mozzarella),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_mozzarella),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_parmigiano),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_parmigiano),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_parmigiano),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_parmigiano),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_eggplant),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_eggplant),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_tomato_sauce),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_tomato_sauce),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_tomato_sauce),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_tomato_sauce),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_bananas),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_bananas),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_bananas),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_bananas),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_oats),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_oats),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_oats),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_oats),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_nuts),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_nuts),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_nuts),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_nuts),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_seed_oil),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_seed_oil),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_seed_oil),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_seed_oil),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_boiled_chestnuts),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_boiled_chestnuts),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_sweet_potatoes),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_sweet_potatoes),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_sweet_potatoes),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_sweet_potatoes),
'autumn'),
	 ((
SELECT
	id
FROM
	ingredient_eggs),
'winter'),
	 ((
SELECT
	id
FROM
	ingredient_eggs),
'spring'),
	 ((
SELECT
	id
FROM
	ingredient_eggs),
'summer'),
	 ((
SELECT
	id
FROM
	ingredient_eggs),
'autumn')
),
recipe_parmigiana AS(
INSERT
	INTO
	public.recipe ("name",
	description,
	nbpeople,
	difficulty,
	"cost",
	idcreator)
VALUES
	 ('Eggplant parmigiana',
'Eggplant parmigiana is one of the most famous and loved Italian recipes. Get stuck into layers of slow-cooked tomato and eggplant – yum!',
6,
3,
2,
(SELECT id FROM creator_remy))
RETURNING id
) ,
recipe_granola AS(
INSERT
	INTO
	public.recipe ("name",
	description,
	nbpeople,
	difficulty,
	"cost",
	idcreator)
VALUES
	 ('Fruit granola',
'Ideal to combine with yogurt, almond milk or as you wish, and enjoy a nutritious and complete food, based on fruits and low in sugar',
6,
1,
2,
(SELECT id FROM creator_remy))
	 RETURNING id
	 ),
recipe_soup AS(INSERT
INTO
	public.recipe ("name",
	description,
	nbpeople,
	difficulty,
	"cost",
	idcreator)
VALUES
	 ('Chestnuts and sweet potatoes soup',
'The most delicious and creamy soup to warm up your winter time!',
4,
1,
2,
(SELECT id FROM creator_remy))
	RETURNING id
	),
recipes_coursetypes AS(
INSERT
	INTO
	public.recipe_coursetype (idrecipe,
	namecoursetype)
VALUES
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
'main course'),
	 ((
SELECT
	id
FROM
	recipe_granola),
'snack'),
	 ((
SELECT
	id
FROM
	recipe_soup),
'starter'),
	 ((
SELECT
	id
FROM
	recipe_soup),
'main course')),
	 step_1_parmigiana AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
1,
'Grill the eggplants.',
30,
60)
	RETURNING nb
	 ),
	 step_2_parmigiana AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
2,
'Chop the mozzarella and grate the parmigiano.',
10,
NULL)
	RETURNING nb
	 ),
	 step_3_parmigiana AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
3,
'In a baking dish, stratify eggplants alternated by tomato sauce, pieces of mozzarella and parmigiano. End with a generous amount of parmigiano.',
10,
NULL)
	 RETURNING nb),
	 step_4_parmigiana AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
4,
'Cook in the oven (static mode) at 180 degrees. Last 10 minutes in grill mode.',
0,
50)
	RETURNING nb
	 ),
	 step_1_granola AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_granola),
1,
'Smash the bananas with a fork.',
5,
0)
	RETURNING nb
	 ),
	 step_2_granola AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_granola),
2,
'Mix it very well together with all other ingredients.',
5,
0)
	RETURNING nb
	 ),
	 step_3_granola AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_granola),
3,
'Cook in the oven at 150 °C for about 1 hour and a half, turning every 30 minutes',
0,
90)
	RETURNING nb
	 ),
	 step_1_soup AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_soup),
1,
'Cut the sweet potatoes and put them to boil together with the chestnuts already cooked, so their flavours can start to combine. Water should cover all the vegetables. Add some salt and spices like cinnamon and thymian, if you like.',
20,
0)
	RETURNING nb
	 ),
	 step_2_soup AS(
	 INSERT
	INTO
	public.step (idrecipe,
	nb,
	instructions,
	preptime,
	cookingtime)
VALUES
	 ((
SELECT
	id
FROM
	recipe_soup),
2,
'Cook for 30 minutes or until the potatoes are soft, then mix everything with a blender to make it creamy. If the consistency is too thick, feel free to add a bit more water. Enjoy! 😋',
0,
30)
	 RETURNING nb
	 ),
steps_ingredients AS(
	 INSERT
	INTO
	public.step_ingredient (idrecipe,
	nbstep,
	idingredient,
	unit,
	quantity)
VALUES
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
(
SELECT
	nb
FROM
	step_3_parmigiana),
(
SELECT
	id
FROM
	ingredient_tomato_sauce),
'gr',
400.00),
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
(
SELECT
	nb
FROM
	step_2_parmigiana),
(
SELECT
	id
FROM
	ingredient_parmigiano),
'gr',
300.00),
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
(
SELECT
	nb
FROM
	step_2_parmigiana),
(
SELECT
	id
FROM
	ingredient_mozzarella),
'gr',
300.00),
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
(
SELECT
	nb
FROM
	step_1_parmigiana),
(
SELECT
	id
FROM
	ingredient_eggplant),
'u',
4.00),
	 ((
SELECT
	id
FROM
	recipe_granola),
(
SELECT
	nb
FROM
	step_1_granola),
(
SELECT
	id
FROM
	ingredient_bananas),
'u',
2.00),
	 ((
SELECT
	id
FROM
	recipe_granola),
(
SELECT
	nb
FROM
	step_2_granola),
(
SELECT
	id
FROM
	ingredient_oats),
'gr',
300.00),
	 ((
SELECT
	id
FROM
	recipe_granola),
(
SELECT
	nb
FROM
	step_2_granola),
(
SELECT
	id
FROM
	ingredient_nuts),
'gr',
100.00),
	 ((
SELECT
	id
FROM
	recipe_granola),
(
SELECT
	nb
FROM
	step_2_granola),
(
SELECT
	id
FROM
	ingredient_sunflower_seeds),
'gr',
50.00),
	 ((
SELECT
	id
FROM
	recipe_granola),
(
SELECT
	nb
FROM
	step_2_granola),
(
SELECT
	id
FROM
	ingredient_seed_oil),
'gr',
40.00),
	 ((
SELECT
	id
FROM
	recipe_soup),
(
SELECT
	nb
FROM
	step_1_soup),
(
SELECT
	id
FROM
	ingredient_boiled_chestnuts),
'gr',
250.00),
	 ((
SELECT
	id
FROM
	recipe_soup),
(
SELECT
	nb
FROM
	step_1_soup),
(
SELECT
	id
FROM
	ingredient_sweet_potatoes),
'gr',
400.00))
INSERT
	INTO
	public.step_tool (idrecipe,
	nbstep,
	idtool)
VALUES
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
(
SELECT
	nb
FROM
	step_4_parmigiana),
(
SELECT
	id
FROM
	tool_oven)),
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
(
SELECT
	nb
FROM
	step_3_parmigiana),
(
SELECT
	id
FROM
	tool_baking_dish)),
	 ((
SELECT
	id
FROM
	recipe_parmigiana),
(
SELECT
	nb
FROM
	step_1_parmigiana),
(
SELECT
	id
FROM
	tool_grill_pan)),
	 ((
SELECT
	id
FROM
	recipe_granola),
(
SELECT
	nb
FROM
	step_3_granola),
(
SELECT
	id
FROM
	tool_oven)),
	 ((
SELECT
	id
FROM
	recipe_soup),
(
SELECT
	nb
FROM
	step_2_soup),
(
SELECT
	id
FROM
	tool_blender))