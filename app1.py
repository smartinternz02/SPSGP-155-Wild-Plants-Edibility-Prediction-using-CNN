from flask import Flask, request, render_template
import numpy as np
import re
import requests
import json
import csv
import pandas as pd
app = Flask(__name__)   

def check(output):
    
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/images/analyze"
    querystring = {"imageUrl":output}
    print(querystring)
    headers = {
        'x-rapidapi-key': "537649ff73msh477f6855911bb13p129cf4jsnd5cb001617b2",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    print(response)
  
    value = response.text
    print(value)
    output=json.loads(value)
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/stats')
def stats():
    return render_template('stats.html')
    
@app.route('/result',methods=['POST'])
def statistics():
    total=0
    output = request.form['image']
    print(output)
    essay = check(output)
    print(essay['nutrition'])
    calories = essay['nutrition']['calories']['value']
    fat = essay['nutrition']['fat']['value']
    protein = essay['nutrition']['protein']['value']
    carbs = essay['nutrition']['carbs']['value']
    data_file = open('data_file.csv', 'w') 
    csv_writer = csv.writer(data_file) 
    count = 0
   
    if count == 0: 
            # Writing headers of CSV file   
        header = ['Calories','Fat','Protein','Carbs']
        csv_writer.writerow(header) 
        count += 1
    # Writing data of CSV file 
    
    d = [calories,fat,protein,carbs]
    print(d)
    csv_writer.writerow(d) 
    data_file.close() 
    df = pd.read_csv("data_file.csv")
    temp = df.to_dict('records')
    columnNames = df.columns.values

    
    return render_template('result.html',records=temp, colnames=columnNames,url=output)
 
 

    
if __name__ == "__main__":
    app.run(debug=True)
