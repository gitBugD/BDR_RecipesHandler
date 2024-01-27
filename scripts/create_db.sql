CREATE TYPE courseTypeEnum 
AS ENUM ('starter', 'main course', 'dessert', 'snack');

CREATE TYPE seasonEnum 
AS ENUM ('winter', 'spring', 'summer', 'autumn');

CREATE TYPE restrictionEnum 
AS ENUM ('vegetarian', 'vegan', 'pork free', 'fish free');

CREATE TYPE unitEnum 
AS ENUM ('gr', 'kg', 'ml', 'l', 'u', 'tsp', 'tbsp', 'c');

CREATE TABLE Creator(
id serial,
name varchar(50) NOT NULL CONSTRAINT CreatorName_NotEmpty CHECK (name != ''),
CONSTRAINT PK_Creator PRIMARY KEY(id),
CONSTRAINT CreatorName_Unique UNIQUE (name)
);

CREATE TABLE Allergen(
id serial,
name varchar(50) NOT NULL CONSTRAINT AllergenName_NotEmpty CHECK (name != ''),
CONSTRAINT PK_Allergen PRIMARY KEY(id),
CONSTRAINT AllergenName_Unique UNIQUE (name)
);

CREATE TABLE Tool(
id serial,
name varchar(50) NOT NULL CONSTRAINT ToolName_NotEmpty CHECK (name != ''),
CONSTRAINT PK_Tool PRIMARY KEY(id),
CONSTRAINT ToolName_Unique UNIQUE (name)
);

CREATE TABLE Ingredient(
id serial,
name varchar(50) NOT NULL CONSTRAINT IngredientName_NotEmpty CHECK (name != ''),
idAllergen int,
CONSTRAINT PK_Ingredient PRIMARY KEY(id),
CONSTRAINT FK_Ingredient_idAllergen FOREIGN KEY(idAllergen) REFERENCES Allergen(id) ON UPDATE CASCADE,
CONSTRAINT IngredientName_Unique UNIQUE (name)
);

CREATE TABLE Ingredient_Season(
idIngredient int,
nameSeason seasonEnum,
CONSTRAINT PK_Ingredient_Season PRIMARY KEY(idIngredient, nameSeason),
CONSTRAINT FK_Ingredient_Season_idIngredient FOREIGN KEY(idIngredient) REFERENCES Ingredient(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Ingredient_Restriction(
idIngredient int,
nameRestriction restrictionEnum,
CONSTRAINT PK_Ingredient_Restriction PRIMARY KEY(idIngredient, nameRestriction),
CONSTRAINT FK_Ingredient_Restriction_idIngredient FOREIGN KEY(idIngredient) REFERENCES Ingredient(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Recipe(
id serial,
name varchar(50) NOT NULL CONSTRAINT RecipeName_NotEmpty CHECK (name != ''),
description text NOT NULL,
nbPeople smallint NOT NULL CONSTRAINT NbPeople_Check CHECK (nbPeople >= 1 AND nbPeople <= 10),
difficulty smallint NOT NULL CONSTRAINT Difficulty_Check CHECK (difficulty >= 0 AND difficulty <= 5),
cost smallint NOT NULL CONSTRAINT Cost_Check CHECK (cost >= 0 AND cost <= 5),
idCreator int NOT NULL,
CONSTRAINT PK_Recipe PRIMARY KEY(id),
CONSTRAINT FK_Recipe_idCreator FOREIGN KEY(idCreator) REFERENCES Creator(id),
CONSTRAINT RecipeName_Unique UNIQUE (name)
);

CREATE TABLE Recipe_CourseType(
idRecipe int,
nameCourseType courseTypeEnum,
CONSTRAINT PK_Recipe_CourseType PRIMARY KEY(idRecipe, nameCourseType),
CONSTRAINT FK_Recipe_CourseType_idRecipe FOREIGN KEY(idRecipe) REFERENCES Recipe(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Step(
idRecipe int,
nb smallint,
instructions text NOT NULL CONSTRAINT Instructions_NotEmpty CHECK (instructions != ''),
prepTime int NOT NULL CONSTRAINT PrepTime_Min CHECK (prepTime > 0 OR cookingTime <> 0), --in minutes
cookingTime int NOT NULL CONSTRAINT CookingTime_Min CHECK (cookingTime >= 0), --in minutes
CONSTRAINT PK_Step PRIMARY KEY(idRecipe, nb),
CONSTRAINT FK_Step_idRecipe FOREIGN KEY(idRecipe) REFERENCES Recipe(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Step_Tool(
idRecipe int,
nbStep smallint,
idTool int,
CONSTRAINT PK_Step_Tool PRIMARY KEY(idRecipe, nbStep, idTool),
CONSTRAINT FK_Step_Tool_idStep FOREIGN KEY(idRecipe, nbStep) REFERENCES Step(idRecipe, nb) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT FK_Step_Tool_idTool FOREIGN KEY(idTool) REFERENCES Tool(id) ON UPDATE CASCADE
);


CREATE TABLE Step_Ingredient(
idRecipe int,
nbStep smallint,
idIngredient int,
unit unitEnum NOT NULL,
quantity numeric(5,2) NOT NULL CONSTRAINT Positive_Quantity CHECK (quantity > 0),
CONSTRAINT PK_Step_Ingredient PRIMARY KEY(idRecipe, nbStep, idIngredient),
CONSTRAINT FK_Step_Ingredient_idStep FOREIGN KEY(idRecipe, nbStep) REFERENCES Step(idRecipe, nb) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT FK_Step_Ingredient_idIngredient FOREIGN KEY(idIngredient) REFERENCES Ingredient(id) ON UPDATE CASCADE
);