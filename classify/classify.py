from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import sys
import json
import operator
import requests

FOOD = {
		"Name" : "Banana",
		"Portions" : "2"
	}

def read():
	return [FOOD[key] for key in FOOD.keys()]


def read(img):

	app = ClarifaiApp(api_key='48f62d7383624823af97e5add9dad7dc')
	
	# get the food model
	model = app.models.get("food-items-v1.0")
	
	# gets the image to be classified and passes it through the model
	
	img = ClImage(filename="./" + img)
	results = model.predict([img])
	
	#accesses the desired results in the json object produced
	results1 = results["outputs"]
	
	results2 = results1[0]
	
	results3 = results2["data"]
	
	results4 = results3["concepts"]
	
	#transforms the results and gets the food with the highest probability
	foodNames = []
	foodProbabilities = []
	
	for result in results4:
		foodNames.append(result.get("name"))
		foodProbabilities.append(result.get("value"))
	
	foods = {}
	for val in range(0, len(foodNames)-1):
		foods[foodNames[val]] = foodProbabilities[val]
	
	topResult = max(foods.iteritems(), key=operator.itemgetter(1))[0]
	
	#getting food macronutrient info
	app_id = "286eba2d" #doesn't use app_id or key at present
	app_key = "30d04c45b0c2df7c764c7620d996d478"
	r = requests.get("https://api.edamam.com/api/food-database/parser?ingr=" + topResult + "&app_id=bea9c802&app_key=a83cf120fba2ebf8c08e56cd0a199852", auth= ("kealanthompson@hotmail.com", "food classify"))
	
	#getting right food info and classifying it based on majority macro
	foodNutrition =r.json()
	nutrition = foodNutrition["parsed"]
	nutrition1 = nutrition[0]
	nutrition2 = nutrition1["food"]
	nutrition3 = nutrition2["nutrients"]
	
	nutrients = {}
	nutrients["protein"] = nutrition3.get("PROCNT")
	nutrients["carbs"] = nutrition3.get("CHOCDF")
	nutrients["fat"] = nutrition3.get("FAT")
	
	mainNutrient = max(nutrients.iteritems(), key=operator.itemgetter(1))[0]
	return mainNutrient