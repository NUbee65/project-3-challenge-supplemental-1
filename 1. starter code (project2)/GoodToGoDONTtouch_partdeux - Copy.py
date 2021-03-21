import requests
import pandas as pd
import json
import sqlalchemy
from sqlalchemy import create_engine
from flask import Flask, request, render_template, jsonify
import pymysql
pymysql.install_as_MySQLdb()
from config import remote_db_endpoint, remote_db_port
from config import remote_db_name, remote_db_user, remote_db_pwd


###################################################
###################################################
###################################################
#   getIngredients()
###################################################
###################################################
##################################################

def getIngredients(query, cuisine, type_of_recipe, calories, cookingMinutes): 
    
    #######################################
    # consider separating this part into a function
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/searchComplex"
    
    # these will come from form controls
    query = query
    cuisine = cuisine
    type_of_recipe = type_of_recipe
    calories = calories
    cookingMinutes = cookingMinutes
    # ranking = "2"
    minCalories = "150"
    maxCalories = "1500"
    # minFat = "5"
    # maxFat = "100"
    # minProtein = "5"
    # maxProtein = "100"
    # minCarbs = "5"
    # maxCarbs = "100"
    
    querystring = {"limitLicense": "<REQUIRED>",
        "offset": "0",
        "number": "10",
        "query": query,
        "cuisine": cuisine,
        "cookingMinutes": cookingMinutes,                   # NEW
        "calories": calories,                               # NEW
        #"includeIngredients": "onions, lettuce, tomato",
        #"excludeIngredients": "coconut, mango",
        #"intolerances": "peanut, shellfish",
        "type": type_of_recipe,
        # "ranking": ranking,
        "minCalories": minCalories,
        "maxCalories": maxCalories,
        # "minFat": minFat,
        # "maxFat": maxFat,
        # "minProtein": minProtein,
        # "maxProtein": maxProtein,
        # "minCarbs": minCarbs,
        # "maxCarbs": maxCarbs,
        "instructionsRequired": "True",
        "addRecipeInformation": "True",
        "fillIngredients": "True",
    }
    
    #NEEDS INDIVIDUAL API KEY
    headers = {
        'x-rapidapi-key': "9e12485098mshdefbf3ff62ef150p1717ddjsn1cf8f48a5741",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    response_json = response.json()
    
    results = response_json['results']
    
    # consider making everything above part of a separate function
    #######################################

    recipe_ingredients = []
    recipe_steps = []
    
    # ingredients stuff
    for result in results:
        try:
            recipe_id = result['id']
            recipe_title = result['title']        
            cooking_minutes = result['cookingMinutes']
            health_score = result['healthScore']
            source_url = result['sourceUrl']
            likes = result['aggregateLikes']                # Brooke modification / previously, it had been 'likes'
            # cuisine = result['cuisines'][0]                 # Brooke addition (my slicing may not work; my method used a df)
            calories_serving = result['calories']           # Brooke addition
            carbohydrates_serving = result['carbs']         # Brooke addition
            servings = result['servings']                   # Brooke addition

            analyzedInstructions = result['analyzedInstructions']
            
        except Exception as e:
            print('--- error with something ---')
            print(result.keys())
            continue 

        instruction_steps = analyzedInstructions[0]['steps']        # Brooke addition

        counter = 0                                                 # Brooke addition

        for item in instruction_steps:                              # Brooke addition
            counter = counter + 1                                   # Brooke addition
            step = item['step']                                     # Brooke addition
            numbered_step = f'{counter}. {step}'                    # Brooke addition
            recipe_steps.append(numbered_step)                      # Brooke addition
        
        for instruction in analyzedInstructions:
            
            steps = instruction['steps']
            
            for step in steps:
                
                ingredients = step['ingredients']
                
                for ingredient in ingredients:
                    
                    ingredient_name = ingredient['name']
                    
                    recipe_ingredient = {
                        'recipe_id': recipe_id,
                        'recipe_title': recipe_title,
                        'ingredient_name': ingredient_name
                    }

                    recipe_ingredients.append(recipe_ingredient)

    recipe_df = pd.DataFrame(recipe_ingredients)

    # dedupe ingredients df
    recipe_df.drop_duplicates(inplace=True)

    return recipe_df


###################################################
#####################
#####################
#   getRecipeMetadata
##################################################
##################################################
##################################################

def getRecipeMetadata(query, cuisine, type_of_recipe, calories, cookingMinutes): 
    
    #######################################
    # consider separating this part into a function
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/searchComplex"
    
    # these will come from form controls
    query = query
    cuisine = cuisine
    type_of_recipe = type_of_recipe
    calories = calories
    cookingMinutes = cookingMinutes
    # ranking = "2"
    minCalories = "150"
    maxCalories = "1500"
    # minFat = "5"
    # maxFat = "100"
    # minProtein = "5"
    # maxProtein = "100"
    # minCarbs = "5"
    # maxCarbs = "100"
    
    querystring = {"limitLicense": "<REQUIRED>",
        "offset": "0",
        "number": "10",
        "query": query,
        "cuisine": cuisine,
        "cookingMinutes": cookingMinutes,                   # NEW
        "calories": calories,                               # NEW
        #"includeIngredients": "onions, lettuce, tomato",
        #"excludeIngredients": "coconut, mango",
        #"intolerances": "peanut, shellfish",
        "type": type_of_recipe,
        # "ranking": ranking,
        "minCalories": minCalories,
        "maxCalories": maxCalories,
        # "minFat": minFat,
        # "maxFat": maxFat,
        # "minProtein": minProtein,
        # "maxProtein": maxProtein,
        # "minCarbs": minCarbs,
        # "maxCarbs": maxCarbs,
        "instructionsRequired": "True",
        "addRecipeInformation": "True",
        "fillIngredients": "True",
    }
    
    headers = {
        'x-rapidapi-key': "9e12485098mshdefbf3ff62ef150p1717ddjsn1cf8f48a5741",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    response_json = response.json()
    
    results = response_json['results']
    
    # consider making everything above part of a separate function
    #######################################

    recipe_metadata_list = []
    # recipe_steps = []
    
    # ingredients stuff
    for result in results:
        try:
            recipe_id = result['id']
            recipe_title = result['title']        
            cooking_minutes = result['cookingMinutes']
            health_score = result['healthScore']
            source_url = result['sourceUrl']
            # image = result['image']
            likes = result['aggregateLikes']                # Brooke modification / previously, it had been 'likes'
            # cuisine = result['cuisines'][0]                 # Brooke addition (my slicing may not work; my method used a df)
            calories_serving = result['calories']           # Brooke addition
            carbohydrates_serving = result['carbs']         # Brooke addition
            servings = result['servings']                   # Brooke addition

            analyzedInstructions = result['analyzedInstructions']
            
        except Exception as e:
            print('--- error with something ---')
            print(result.keys())
            continue

        # 'directions': recipe_steps
        # # we need to figure out what this block is...
        # for result in results:
        #     servings = result['servings']     


        instruction_steps = analyzedInstructions[0]['steps']        # Brooke addition

        counter = 0
        
        recipe_steps = []                                                 # Brooke addition

        for item in instruction_steps:                              # Brooke addition
            counter = counter + 1                                   # Brooke addition
            step = item['step']                                     # Brooke addition
            numbered_step = f'{counter}. {step}'                    # Brooke addition
            recipe_steps.append(numbered_step)                      # Brooke addition
                    
        recipe_metadata = {
            'recipe_id': recipe_id,
            'recipe_title': recipe_title,
            'cooking_minutes': cooking_minutes,
            'health_score': health_score,
            'source_url': source_url,
            # 'image': image,
            'likes': likes,
            'calories_serving': calories_serving,
            'carbohydrates_serving': carbohydrates_serving,
            'servings': servings,
            'recipe_steps': recipe_steps
        }

        # will need to rename this
        recipe_metadata_list.append(recipe_metadata)

    recipe_metadata_df = pd.DataFrame(recipe_metadata_list)

    # dedupe ingredients df
    # recipe_metadata_df.drop_duplicates(inplace=True)

    return recipe_metadata_df











###################################################
#####################
#####################
#   getQuantities
##################################################
##################################################
##################################################

def getQuantities(query, cuisine):
    
    #######################################
    # consider separating this part into a function
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/searchComplex"

    url2 = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={headers2}"
    
    # these will come from form controls
    query = query
    cuisine = cuisine
    type_of_recipe = 'main course'
    ranking = "2"
    minCalories = "150"
    maxCalories = "1500"
    minFat = "5"
    maxFat = "100"
    minProtein = "5"
    maxProtein = "100"
    minCarbs = "5"
    maxCarbs = "100"
    
    querystring = {"limitLicense": "<REQUIRED>",
        "offset": "0",
        "number": "10",
        "query": query,
        "cuisine": cuisine,
        #"includeIngredients": "onions, lettuce, tomato",
        #"excludeIngredients": "coconut, mango",
        #"intolerances": "peanut, shellfish",
        "type": type_of_recipe,
        "ranking": ranking,
        "minCalories": minCalories,
        "maxCalories": maxCalories,
        "minFat": minFat,
        "maxFat": maxFat,
        "minProtein": minProtein,
        "maxProtein": maxProtein,
        "minCarbs": minCarbs,
        "maxCarbs": maxCarbs,
        "instructionsRequired": "True",
        "addRecipeInformation": "True",
        "fillIngredients": "True",
    }
    
    headers = {
        'x-rapidapi-key': "9e12485098mshdefbf3ff62ef150p1717ddjsn1cf8f48a5741",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

    headers2 = 'aaef90d4d7604737bba08d638069d857'               # PartDeux Addition
    
    response = requests.get(url, headers=headers, params=querystring)
    
    response_json = response.json()
    
    results = response_json['results']
    
    # consider making everything above part of a separate function
    #######################################

    # recipe_metadata_list = []
    
    # create an Empty DataFrame object with column headers    
    column_names = ["recipe_id", "recipe_title", "ingredient_id", "ingredient", "amount_unit", "amount", "unit"]
    recipe_quantities_df = pd.DataFrame(columns = column_names)
    
    # ingredients stuff
    for result in results:
        try:
            recipe_id = result['id']
            print(recipe_id)
            recipe_title = result['title']

            response2 = requests.get(url2)
            json_data2 = response2.json()
            df2 = pd.DataFrame(json_data2["extendedIngredients"])
            df3 = df2[['id', 'name', 'original', 'amount', 'unit']]
            df4 = df3.rename(columns={"id": "ingredient_id", "name": "ingredient", "original": "amount_unit"})
            df4.insert(0, "recipe_id", recipe_id)
            df4.insert(1, "recipe_title", recipe_title)
            
        except Exception as e:
            print('--- error with something ---')
            print(result.keys())
            continue

        recipe_quantities_df.merge(df4, how='outer')

        # recipe_quantities_etal = {
        #    'recipe_id': recipe_id,
        #    'recipe_title': recipe_title            
        #}

        # will need to rename this
        # recipe_metadata_list.append(recipe_metadata)

    # recipe_metadata_df = pd.DataFrame(recipe_metadata_list)

    # dedupe ingredients df
    # recipe_quantities_df.drop_duplicates(inplace=True)

    return recipe_quantities_df




###################################################
#####################
#####################
#   Connect to Database
##################################################
##################################################
##################################################

cloud_engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")

cloud_conn = cloud_engine.connect()

#%% Querying the database
query = '''
        SELECT DISTINCT
            ingredient,
            price,
            title,
            size
        FROM
            products_subset
        '''

products_subset = pd.read_sql(query, cloud_conn)

products_subset.head()

cloud_conn.close()




app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/api/ingredients')
def ingredients():
    
    query = request.args.get('query')
    cuisine = request.args.get('cuisine')
    cookingMinutes = request.args.get('cookingMinutes')
    calories = request.args.get('calories')
    type_of_recipe = request.args.get('type_of_recipe')
    
    recipe_df = getIngredients(query, cuisine, cookingMinutes, type_of_recipe, calories)
    
    recipe_json = recipe_df.to_json(orient='records')
    
    return recipe_json

@app.route('/api/recipemetadata')
def recipemetadata():
    
    query = request.args.get('query')
    cuisine = request.args.get('cuisine')
    cookingMinutes = request.args.get('cookingMinutes')
    calories = request.args.get('calories')
    type_of_recipe = request.args.get('type_of_recipe')
    
    recipe_df = getRecipeMetadata(query, cuisine, cookingMinutes, type_of_recipe, calories)
    
    recipe_json = recipe_df.to_json(orient='records')
    
    return recipe_json

@app.route('/api/recipequantities')
def recipequantities():
    
    query = request.args.get('query')
    cuisine = request.args.get('cuisine')
    
    
    recipe_df = getQuantities(query, cuisine)
    
    recipe_json = recipe_df.to_json(orient='records')
    
    return recipe_json

@app.route('/ingredientsWithPrices')
def productsFromScrape():
    products_json = products_subset.to_json(orient='records')
    return(products_json)

if __name__ == '__main__':
    app.run(debug=True)